..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Reset Volume State with Driver Involved
==========================================

https://blueprints.launchpad.net/cinder/+spec/reset-state-with-driver

The python-cinderclient reset-state command allows an admin to change the state
of a volume in the cinder database, but there is no change to the backend
storage. This means that an admin can set a volume to 'Available' when the
volume is, in fact, still attached to a compute instance. This new
functionality will submit the request to the volume driver first, and then
proceed to update the database. A '--force' flag would allow a volume driver
exception to be ignored, or possibly skip the request to the driver altogether.


Problem description
===================

It is not uncommon to have a volume stuck in a state that prevents the user
from using the volume or changing state, i.e. 'attaching', 'deleting',
'creating', 'detaching'. The python-cinderclient has the command 'reset-state'
to allow an admin to change the volume state in the cinder database to any
state desired.
In order to fix the problem in a safe and robust way, however, the admin must
check the state of the volume with regards to the backend storage and Nova. Is
the volume attached according to the metadata of the backend? Is there an Iscsi
connection (or FC) to the compute host? Does Nova database list the volume as
attached? Does the instance virsh state or <instance_id>.xml list the volume as
attached? This spec will only address the cinder database and backend driver
aspects. The changes required to set state properly for Nova are beyond the
current scope.

Example: Volume is stuck in 'attaching' but physical volume is not attached
to the nova compute host and Nova instance still sees the volume as unattached.
    1. Admin issues command 'reset-state <volume_id>' (default state is
           available) via python-cinderclient
    2. API call is sent to VolumeManager
    3. VolumeManager issues RPC call to VolumeDriver
           a. If driver has implemented 'reset_state(...)', driver attempts
              to set volume to desired state
              i. if successful, function returns normally
              ii. if unsuccessful, an exception is thrown
           b. If driver has not implemented 'reset-state(...), VolumeManager
              returns NotImplementedError()
    4. VolumeManger issues reset_status(...) to update database

A '--force' flag would allow the admin to proceed with the Cinder database
update regardless of the volume driver. This could mean attempting to set the
proper state via the driver and ignoring any exceptions, or possibly skipping
the call to the VolumeDriver altogether.

Currently, cinderclient reset-state valid values are "available," "error,"
"creating," "deleting," or "error_deleting." Default is "available." The only
state that makes sense for the driver is "available", so the other states
could be ignored. It might be desirable to add a state to the python-
cinderclient to allow the admin to set to 'in-use' and add the proper plumbing
to the VolumeDriver to accomplish this.

Proposed change
===============

1. move api/contrib/admin_actions.py:_reset_status(...) from AdminController
   to VolumeAdminController
2. change _reset_status(...) to call self.volume_api.reset_status(...)
3. add reset_status(..) to the volume/API class
4. if desired state == available
    a. volume/api.py:reset_status(...) will call detach() or
        self.volume_rpcapi.detach_volume(...)
    b. VolumeDriver base class raises NotImplementedError()
    c. VolumeDriver subclasses implement detach_volume or re-use existing
5. For any desired state, change database using logic currently in
   api/contrib/admin_actions.py:_reset_status(....)

It might be desirable to plumb the state 'in-use' at this time, and make
the change to python-cinderclient to make that state available.

Alternatives
------------

Leave things as they are, requiring the admin to make manual changes using APIs
or commands on the back end storage to keep the state in sync. This requires
extra work and possibility for error.
The flow from cinderclient to the VolumeDriver could be altered. Suggestions
are welcome.


Data model impact
-----------------

None

REST API impact
---------------

The existing reset-state api will be used:
POST /v2/{tenant_id}/volumes/{volume_id}/action -d '{"os-reset_status": {"status": "available"}}'

It may be desired to add the state 'in-use' to the JSON schema

Security impact
---------------

None

Notifications impact
--------------------

None

Other end user impact
---------------------

The addition of a '--force' option to ignore driver exceptions or bypass a
call to the driver would require a change to the python-cinderclient. This
would be backwards compatible on the client side, but not on the server.
If desired, the python-cinderclient would also need a change to add the
'in-use' state as an option.

Performance Impact
------------------

The addition of a call to the driver to detach a volume when setting the state
to 'available' may add a noticable amount of time to 'reset-state'.

Other deployer impact
---------------------

None

Developer impact
----------------

None

Implementation
==============

Assignee(s)
-----------

Primary assignee:
scott-dangelo

Work Items
----------

1. move api/contrib/admin_actions.py:_reset_status(...) from AdminController
   to VolumeAdminController
2. change _reset_status(...) to call self.volume_api.reset_status(...)
3. add reset_status(..) to the volume/API class
4. change volume/api.py:reset_status(...) to call detach() or
        self.volume_rpcapi.detach_volume(...)
5. change VolumeDriver base class raises NotImplementedError()
6. add code to volume/API/reset_status() to change database using logic
   currently in api/contrib/admin_actions.py:_reset_status(....)

Possibly:
7. change volume/api.py:reset_status(...) to call attach() or
        self.volume_rpcapi.attach_volume(...)


Dependencies
============

None

Testing
=======

Tempests tests should be added if the python-cinderclient is changed to add
a '--force' option, and also if a state 'in-use' is added.

Documentation Impact
====================

The documents currently do not state what the python-cinderclient does when
'reset-state' is called, so that would not have to change. Adding a '--force'
option and/or a state of 'in-use' would require doc changes.


References
==========

