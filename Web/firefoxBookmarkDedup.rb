# Did Mozilla F1 and Firefox Sync manage to duplicate your bookmarks 57814 times (like they did mine)?
# Did CheckPlaces and other misc addons completely fail at the task of removing duplicate bookmarks?
# Does the bookmarks manager grind to a halt even selecting an item?
# This is the fix for you..

# Backup the bookmarks in Firefox using the Backup function 
# (from the star icon in the bookmarks manager) to JSON.

# Invoke this script as following:
# ruby dupefixer.rb /Users/yourname/Desktop/bookmarks.json
# This will generate bookmarks.json.fixed.json in the working directory.
# You can then restore this file to Firefox using the same menu 
# used to back up by selecting Restore > Choose File.

# You might have to nuke your old places.sqlite and 
# fully reset your Sync profile as well..

require 'rubygems' # IDGAF
require 'json'
require 'json/add/core'

$delete_count = 0

def usage
  puts "#{__FILE__} [bookmarks.json]"
end

def remove_duplicates filename
  orig_bookmarks = JSON.parse File.open(filename).read
  bookmark_count = Hash.new
  
  orig_bookmarks['children'].each do |bookmarks_folder|
    # mark down any duplicates  
    bookmarks_folder['children'].each do |bookmark|
      bookmark_count[bookmark['uri']] = bookmark_count.has_key?(bookmark['uri']) ? (bookmark_count[bookmark['uri']] + 1) : 1
    end
  end
  
  orig_bookmarks['children'].each do |bookmarks_folder|
    # delete duplicates
    bookmarks_folder['children'].delete_if do |bookmark|
      if bookmark_count[bookmark['uri']] > 1 then
        bookmark_count[bookmark['uri']] = bookmark_count[bookmark['uri']] - 1
        $delete_count = $delete_count + 1
        puts "#{$delete_count} bookmarks deleted so far, last deleted was at #{bookmark['uri']}"
        true
      else
        false
      end
    end
  end
  
  orig_bookmarks
end

if ARGV.first.nil?
  usage
else
  outfile = File.open("#{ARGV.first}.fixed.json", 'w')
  outfile.write(JSON.generate(remove_duplicates(ARGV.first)))
  outfile.close
end

puts "Done removing duplicates, #{$delete_count} bookmarks removed total"
