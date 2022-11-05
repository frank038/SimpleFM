### main program
# can use: 1 - the user mimeapps.list (in $HOME/.config/mimeapps.list) or 0 - that in the program
USER_MIMEAPPSLIST=0
# set the terminal to use or leave "" for the default one
USER_TERMINAL=""
# directory to open - full path or HOME
FOLDER_TO_OPEN = "HOME"
# template folder
TEMPLATE_DIR="Templates"
# multi items drag picture: 0 use simple icon - 1 enable extended icon
USE_EXTENDED_DRAG_ICON=1
# x offset of each icon if USE_EXTENDED_DRAG_ICON is enabled
X_EXTENDED_DRAG_ICON=40
# y offset of each icon if USE_EXTENDED_DRAG_ICON is enabled
Y_EXTENDED_DRAG_ICON=20
# limit the number of icon overlay if USE_EXTENDED_DRAG_ICON is enabled
NUM_OVERLAY=20
# show the alternative view button: 0 no - 1 yes
ALTERNATE_VIEW = 0
# Open with... dialog: 0 simple - 1 list installed applications
OPEN_WITH = 1
# mouse middle button behaviour: 0 open the folder in the same view - 1 open the folder in another tab
IN_SAME = 1
# thumbnailers: 0 no - 1 yes
USE_THUMB = 0
# use custom icons for folders: 0 no - 1 yes
USE_FOL_CI = 0
# icon cell width - greater than ICON_SIZE
ITEM_WIDTH = 80
# icon cell width alternative view - greater than ICON_SIZE
ITEM_WIDTH_ALT = 48
# icon cell height
ITEM_HEIGHT = 80
# icon cell height alternative view
ITEM_HEIGHT_ALT = 48
# icon size
ICON_SIZE = 48
# icon size alternative view
ICON_SIZE_ALT = 24
# thumb size: greater than ICON_SIZE - same size of ICON_SIZE to disable bigger thumbnailers
THUMB_SIZE = 64
# other icons size: link and permissions
ICON_SIZE2 = 14
# other icons size alternative view: link and permissions
ICON_SIZE2_ALT = 14
# space between items
ITEM_SPACE = 25
# the size of the circle at top-left of each item
CIRCLE_SIZE=14
# the circle color in the form #AARRGGBB - arancione #88DF5E0B
CIRCLE_COLOR="#CA3042"
# tick symbol
TICK_CHAR="✓"
# tick size in pixels
TICK_SIZE=14
# tick symbol color
TICK_COLOR="white"
# menu highlight colour: use "" to use the default style - blu #5AA7F8
MENU_H_COLOR=""
# service buttons size: 0 to disable
BUTTON_SIZE=18
# show delete context menu entry that bypass the trashcan: 0 no - 1 yes
USE_DELETE = 1
# load the trash module: 0 no - 1 yes
USE_TRASH = 1
# load the media: 0 no - 1 yes
USE_MEDIA = 1
# media to skip, comma separated values in the form "/dev/xxx" - not reccomanded for removable ones
MEDIA_SKIP=[]
# Paste and Merge, how to backup the new files: 0 add progressive number
# in the form _(#) - 1 add date and time (without checking eventually
# existing file at destination with same date and time suffix) 
# in the form _yy.mm.dd_hh.mm.ss
USE_DATE = 1
# use background colour in the listview widgets: 0 no - 1 yes
USE_BACKGROUND_COLOUR = 1
# list of opened folders - widget type: 0 flow widget - 1 scroll widget
FLOW_WIDGET = 0
# listview background color: red, green, blue
ORED = 235
OGREEN = 235
OBLUE = 235
# treeview alternate background color: red, green, blue (0 - 255)
ORED2 = 223
OGREEN2 = 223
OBLUE2 = 223
# use listview and treeview text color: 0 no - 1 only alternate view - 2 main view too
TCOLOR = 0
# listview and treeview text color: red, green, blue (0 - 255)
TRED = 0
TGREEN = 0
TBLUE = 0
# icon theme name - if the qt5ct program overrides this use ""
ICON_THEME = ""
# creation data and time of the item in the property dialog: 0 use os.stat - 1 use functions from bash (should be precise)
DATE_TIME = 1
# use additional data in each item: 0 no - 1 yes 
USE_AD = 0
# dialog windows width
DIALOGWIDTH=200
### needed for qt5archiver
# usually 7z - or 7za
COMMAND_EXTRACTOR="7z"
# pkexec: 1 use default program - 2 use internal command
PKEXEC_PROG=1

### needed by pythumb
# use thumbnailer in the home dir only: 0 no - 1 yes
USE_THUMB_HOME_ONLY=1
# use borders: 0 no - 1 yes - 2 yes and use the internal program mode
USE_BORDERS=1
# 
BORDER_WIDTH=2
# border color of the thumbnails - 0 to 255 per colour
BORDER_COLOR_R = 0
BORDER_COLOR_G = 0
BORDER_COLOR_B = 0
# thumbnail images cache
XDG_CACHE_LARGE = "sh_thumbnails/large/"
