#!/usr/bin/env python3

import os
from xdg import DesktopEntry
from xdg import IconTheme
# to get the language
import locale

#######################

class getMenu():
    
    #def __init__(self, app_dirs_user, app_dirs_system):
    def __init__(self):
        # the dirs of the application files
        app_dirs_user = [os.path.expanduser("~")+"/.local/share/applications"]
        app_dirs_system = ["/usr/share/applications", "/usr/local/share/applications"]

        # main categories
        # removed "Audio" e "Video" main categories
        self.freedesktop_main_categories = ["AudioVideo","Development",
                                      "Education","Game","Graphics","Network",
                                      "Office","Settings","System","Utility"]
        # additional categories
        self.development_extended_categories = ["Building","Debugger","IDE","GUIDesigner",
                                          "Profiling","RevisionControl","Translation",
                                          "Database","WebDevelopment"]
        
        self.office_extended_categories = ["Calendar","ContanctManagement","Office",
                                     "Dictionary","Chart","Email","Finance","FlowChart",
                                     "PDA","ProjectManagement","Presentation","Spreadsheet",
                                     "WordProcessor","Engineering"]
        
        self.graphics_extended_categories = ["2DGraphics","VectorGraphics","RasterGraphics",
                                       "3DGraphics","Scanning","OCR","Photography",
                                       "Publishing","Viewer"]
        
        self.utility_extended_categories = ["TextTools","TelephonyTools","Compression",
                                      "FileTools","Calculator","Clock","TextEditor",
                                      "Documentation"]
        
        self.settings_extended_categories = ["DesktopSettings","HardwareSettings",
                                       "Printing","PackageManager","Security",
                                       "Accessibility"]
        
        self.network_extended_categories = ["Dialup","InstantMessaging","Chat","IIRCClient",
                                      "FileTransfer","HamRadio","News","P2P","RemoteAccess",
                                      "Telephony","VideoConference","WebBrowser"]
        
        # added "Audio" and "Video" main categories
        self.audiovideo_extended_categories = ["Audio","Video","Midi","Mixer","Sequencer","Tuner","TV",
                                         "AudioVideoEditing","Player","Recorder",
                                         "DiscBurning"]
        
        self.game_extended_categories = ["ActionGame","AdventureGame","ArcadeGame",
                                   "BoardGame","BlockGame","CardGame","KidsGame",
                                   "LogicGame","RolePlaying","Simulation","SportGame",
                                   "StrategyGame","Amusement","Emulator"]
        
        self.education_extended_categories = ["Art","Construction","Music","Languages",
                                        "Science","ArtificialIntelligence","Astronomy",
                                        "Biology","Chemistry","ComputerScience","DataVisualization",
                                        "Economy","Electricity","Geography","Geology","Geoscience",
                                        "History","ImageProcessing","Literature","Math","NumericAnalysis",
                                        "MedicalSoftware","Physics","Robots","Sports","ParallelComputing",
                                        "Electronics"]
        
        self.system_extended_categories = ["FileManager","TerminalEmulator","FileSystem",
                                     "Monitor","Core"]
        
        # arguments in the exec fiels
        self.execArgs = [" %f", " %F", " %u", " %U", " %d", " %D", " %n", " %N", " %k", " %v"]
        
        # the default
        self.locale_lang = "en"
        try:
            self.locale_lang = locale.getlocale()[0].split("_")[0]
        except:
            self.locale_lang = "en"

        # list of all catDesktop - one for desktop file
        self.info_desktop = []
        # list of all desktop files found
        self.lists = []
        # fill self.info_desktop
        self.fpop(app_dirs_system)
        self.fpop(app_dirs_user)
        
    # return the lists
    def retList(self):
        #list_one = sorted(self.lists, key=lambda x: x[1].lower(), reverse=False)
        #return list_one
        return self.lists
    
#############################

    def fpop(self, ap_dir):
        for ddir in ap_dir:
            if os.path.exists(ddir):
                for ffile in os.listdir(ddir):
                    if not ffile.lower().endswith(".desktop"):
                        continue
                    #
                    fpath = os.path.join(ddir, ffile)
                    try:
                        entry = DesktopEntry.DesktopEntry(fpath)
                        ftype = entry.getType()
                        if ftype != "Application":
                            continue
                        hidden = entry.getHidden()
                        nodisplay = entry.getNoDisplay()
                        # do not show those marked as hidden or not to display
                        if hidden or nodisplay:
                            continue
                        # item.name
                        fname = entry.getName()
                        # item.path
                        # fpath
                        # category
                        ccat = entry.getCategories()
                        fcategory = self.get_category(ccat)
                        ## item.name.lower()
                        # fname_lower = fname.lower()
                        # pexec (executable)
                        fexec = entry.getExec()
                        if fexec[0:5] == "$HOME":
                            fexec = "~"+fexec[5:]
                        # check for arguments and remove them
                        # if fexec[-3:] in self.execArgs:
                            # fexec = fexec[:-3]
                        for aargs in self.execArgs:
                            if aargs in fexec:
                                fexec = fexec.strip(aargs)
                        # # icon
                        # ficon = entry.getIcon()
                        # # comment
                        # fcomment = entry.getComment()
                        ###
                        self.lists.append([fname, fcategory or "Missed", fexec])
                    except:
                        pass

    #
    def get_category(self, ccat):
        if ccat == []:
            return "Missed"
        for cccat in ccat:
            # search in the main categories first
            if cccat in self.freedesktop_main_categories:
                # from AudioVideo to Multimedia
                if cccat == "AudioVideo":
                    return "Multimedia"
                return cccat
            elif cccat in self.development_extended_categories:
                return "Development"
            elif cccat in self.office_extended_categories:
                return "Office"
            elif cccat in self.graphics_extended_categories:
                return "Graphics"
            elif cccat in self.utility_extended_categories:
                return "Utility"
            elif cccat in self.settings_extended_categories:
                return "Settings"
            elif cccat in self.network_extended_categories:
                return "Network"
            elif cccat in self.audiovideo_extended_categories:
                # return "AudioVideo"
                return "Multimedia"
            elif cccat in self.game_extended_categories:
                return "Game"
            elif cccat in self.education_extended_categories:
                return "Education"
            elif cccat in self.system_extended_categories:
                return "System"
            # # ???
            # else:
                # return "Missed"
