from rdkit import Chem
from collections import namedtuple
from typing import List, Tuple

from rdkit.Chem import Draw
from rdkit.Chem.Draw import DrawingOptions, rdMolDraw2D

# Local imports
import linchemin.cheminfo.functions as cif

Color = namedtuple("Color", 'name, red, green, blue, hex_string, color_blind')


class ColorMap:
    """
    class to host colors in RGB and hexadecimal format
    https://www.webucator.com/article/python-color-constants-module/
    https://cloford.com/resources/colours/500col.htm

    color blind friendly colors are
    okabe_ito colormap from https://davidmathlogic.com/colorblind
    ibm colormap from https://davidmathlogic.com/colorblind
    okabe_ito colormap from https://jfly.uni-koeln.de/color/

    the class provides methods to search colors by:
    1) name
    2) rgb_tuple
        2.1) identical tuple
        2.2) similar tuple
    3) hex_string
    4) color_blind attribute

    """

    def __init__(self):
        self.colors = [Color(name='aliceblue', red=240, green=248, blue=255, hex_string='#F0F8FF', color_blind=None),
                       Color(name='antiquewhite', red=250, green=235, blue=215, hex_string='#FAEBD7', color_blind=None),
                       Color(name='antiquewhite1', red=255, green=239, blue=219, hex_string='#FFEFDB',
                             color_blind=None),
                       Color(name='antiquewhite2', red=238, green=223, blue=204, hex_string='#EEDFCC',
                             color_blind=None),
                       Color(name='antiquewhite3', red=205, green=192, blue=176, hex_string='#CDC0B0',
                             color_blind=None),
                       Color(name='antiquewhite4', red=139, green=131, blue=120, hex_string='#8B8378',
                             color_blind=None),
                       Color(name='aqua', red=0, green=255, blue=255, hex_string='#00FFFF', color_blind=None),
                       Color(name='aquamarine1', red=127, green=255, blue=212, hex_string='#7FFFD4', color_blind=None),
                       Color(name='aquamarine2', red=118, green=238, blue=198, hex_string='#76EEC6', color_blind=None),
                       Color(name='aquamarine3', red=102, green=205, blue=170, hex_string='#66CDAA', color_blind=None),
                       Color(name='aquamarine4', red=69, green=139, blue=116, hex_string='#458B74', color_blind=None),
                       Color(name='azure1', red=240, green=255, blue=255, hex_string='#F0FFFF', color_blind=None),
                       Color(name='azure2', red=224, green=238, blue=238, hex_string='#E0EEEE', color_blind=None),
                       Color(name='azure3', red=193, green=205, blue=205, hex_string='#C1CDCD', color_blind=None),
                       Color(name='azure4', red=131, green=139, blue=139, hex_string='#838B8B', color_blind=None),
                       Color(name='banana', red=227, green=207, blue=87, hex_string='#E3CF57', color_blind=None),
                       Color(name='beige', red=245, green=245, blue=220, hex_string='#F5F5DC', color_blind=None),
                       Color(name='bisque1', red=255, green=228, blue=196, hex_string='#FFE4C4', color_blind=None),
                       Color(name='bisque2', red=238, green=213, blue=183, hex_string='#EED5B7', color_blind=None),
                       Color(name='bisque3', red=205, green=183, blue=158, hex_string='#CDB79E', color_blind=None),
                       Color(name='bisque4', red=139, green=125, blue=107, hex_string='#8B7D6B', color_blind=None),
                       Color(name='black', red=0, green=0, blue=0, hex_string='#000000', color_blind=None),
                       Color(name='blanchedalmond', red=255, green=235, blue=205, hex_string='#FFEBCD',
                             color_blind=None),
                       Color(name='blue', red=0, green=0, blue=255, hex_string='#0000FF', color_blind=None),
                       Color(name='blue2', red=0, green=0, blue=238, hex_string='#0000EE', color_blind=None),
                       Color(name='blue3', red=0, green=0, blue=205, hex_string='#0000CD', color_blind=None),
                       Color(name='blue4', red=0, green=0, blue=139, hex_string='#00008B', color_blind=None),
                       Color(name='blueviolet', red=138, green=43, blue=226, hex_string='#8A2BE2', color_blind=None),
                       Color(name='brick', red=156, green=102, blue=31, hex_string='#9C661F', color_blind=None),
                       Color(name='brown', red=165, green=42, blue=42, hex_string='#A52A2A', color_blind=None),
                       Color(name='brown1', red=255, green=64, blue=64, hex_string='#FF4040', color_blind=None),
                       Color(name='brown2', red=238, green=59, blue=59, hex_string='#EE3B3B', color_blind=None),
                       Color(name='brown3', red=205, green=51, blue=51, hex_string='#CD3333', color_blind=None),
                       Color(name='brown4', red=139, green=35, blue=35, hex_string='#8B2323', color_blind=None),
                       Color(name='burlywood', red=222, green=184, blue=135, hex_string='#DEB887', color_blind=None),
                       Color(name='burlywood1', red=255, green=211, blue=155, hex_string='#FFD39B', color_blind=None),
                       Color(name='burlywood2', red=238, green=197, blue=145, hex_string='#EEC591', color_blind=None),
                       Color(name='burlywood3', red=205, green=170, blue=125, hex_string='#CDAA7D', color_blind=None),
                       Color(name='burlywood4', red=139, green=115, blue=85, hex_string='#8B7355', color_blind=None),
                       Color(name='burntsienna', red=138, green=54, blue=15, hex_string='#8A360F', color_blind=None),
                       Color(name='burntumber', red=138, green=51, blue=36, hex_string='#8A3324', color_blind=None),
                       Color(name='cadetblue', red=95, green=158, blue=160, hex_string='#5F9EA0', color_blind=None),
                       Color(name='cadetblue1', red=152, green=245, blue=255, hex_string='#98F5FF', color_blind=None),
                       Color(name='cadetblue2', red=142, green=229, blue=238, hex_string='#8EE5EE', color_blind=None),
                       Color(name='cadetblue3', red=122, green=197, blue=205, hex_string='#7AC5CD', color_blind=None),
                       Color(name='cadetblue4', red=83, green=134, blue=139, hex_string='#53868B', color_blind=None),
                       Color(name='cadmiumorange', red=255, green=97, blue=3, hex_string='#FF6103', color_blind=None),
                       Color(name='cadmiumyellow', red=255, green=153, blue=18, hex_string='#FF9912', color_blind=None),
                       Color(name='carrot', red=237, green=145, blue=33, hex_string='#ED9121', color_blind=None),
                       Color(name='chartreuse1', red=127, green=255, blue=0, hex_string='#7FFF00', color_blind=None),
                       Color(name='chartreuse2', red=118, green=238, blue=0, hex_string='#76EE00', color_blind=None),
                       Color(name='chartreuse3', red=102, green=205, blue=0, hex_string='#66CD00', color_blind=None),
                       Color(name='chartreuse4', red=69, green=139, blue=0, hex_string='#458B00', color_blind=None),
                       Color(name='chocolate', red=210, green=105, blue=30, hex_string='#D2691E', color_blind=None),
                       Color(name='chocolate1', red=255, green=127, blue=36, hex_string='#FF7F24', color_blind=None),
                       Color(name='chocolate2', red=238, green=118, blue=33, hex_string='#EE7621', color_blind=None),
                       Color(name='chocolate3', red=205, green=102, blue=29, hex_string='#CD661D', color_blind=None),
                       Color(name='chocolate4', red=139, green=69, blue=19, hex_string='#8B4513', color_blind=None),
                       Color(name='cobalt', red=61, green=89, blue=171, hex_string='#3D59AB', color_blind=None),
                       Color(name='cobaltgreen', red=61, green=145, blue=64, hex_string='#3D9140', color_blind=None),
                       Color(name='coldgrey', red=128, green=138, blue=135, hex_string='#808A87', color_blind=None),
                       Color(name='coral', red=255, green=127, blue=80, hex_string='#FF7F50', color_blind=None),
                       Color(name='coral1', red=255, green=114, blue=86, hex_string='#FF7256', color_blind=None),
                       Color(name='coral2', red=238, green=106, blue=80, hex_string='#EE6A50', color_blind=None),
                       Color(name='coral3', red=205, green=91, blue=69, hex_string='#CD5B45', color_blind=None),
                       Color(name='coral4', red=139, green=62, blue=47, hex_string='#8B3E2F', color_blind=None),
                       Color(name='cornflowerblue', red=100, green=149, blue=237, hex_string='#6495ED',
                             color_blind=None),
                       Color(name='cornsilk1', red=255, green=248, blue=220, hex_string='#FFF8DC', color_blind=None),
                       Color(name='cornsilk2', red=238, green=232, blue=205, hex_string='#EEE8CD', color_blind=None),
                       Color(name='cornsilk3', red=205, green=200, blue=177, hex_string='#CDC8B1', color_blind=None),
                       Color(name='cornsilk4', red=139, green=136, blue=120, hex_string='#8B8878', color_blind=None),
                       Color(name='crimson', red=220, green=20, blue=60, hex_string='#DC143C', color_blind=None),
                       Color(name='cyan2', red=0, green=238, blue=238, hex_string='#00EEEE', color_blind=None),
                       Color(name='cyan3', red=0, green=205, blue=205, hex_string='#00CDCD', color_blind=None),
                       Color(name='cyan4', red=0, green=139, blue=139, hex_string='#008B8B', color_blind=None),
                       Color(name='darkgoldenrod', red=184, green=134, blue=11, hex_string='#B8860B', color_blind=None),
                       Color(name='darkgoldenrod1', red=255, green=185, blue=15, hex_string='#FFB90F',
                             color_blind=None),
                       Color(name='darkgoldenrod2', red=238, green=173, blue=14, hex_string='#EEAD0E',
                             color_blind=None),
                       Color(name='darkgoldenrod3', red=205, green=149, blue=12, hex_string='#CD950C',
                             color_blind=None),
                       Color(name='darkgoldenrod4', red=139, green=101, blue=8, hex_string='#8B6508', color_blind=None),
                       Color(name='darkgray', red=169, green=169, blue=169, hex_string='#A9A9A9', color_blind=None),
                       Color(name='darkgreen', red=0, green=100, blue=0, hex_string='#006400', color_blind=None),
                       Color(name='darkkhaki', red=189, green=183, blue=107, hex_string='#BDB76B', color_blind=None),
                       Color(name='darkolivegreen', red=85, green=107, blue=47, hex_string='#556B2F', color_blind=None),
                       Color(name='darkolivegreen1', red=202, green=255, blue=112, hex_string='#CAFF70',
                             color_blind=None),
                       Color(name='darkolivegreen2', red=188, green=238, blue=104, hex_string='#BCEE68',
                             color_blind=None),
                       Color(name='darkolivegreen3', red=162, green=205, blue=90, hex_string='#A2CD5A',
                             color_blind=None),
                       Color(name='darkolivegreen4', red=110, green=139, blue=61, hex_string='#6E8B3D',
                             color_blind=None),
                       Color(name='darkorange', red=255, green=140, blue=0, hex_string='#FF8C00', color_blind=None),
                       Color(name='darkorange1', red=255, green=127, blue=0, hex_string='#FF7F00', color_blind=None),
                       Color(name='darkorange2', red=238, green=118, blue=0, hex_string='#EE7600', color_blind=None),
                       Color(name='darkorange3', red=205, green=102, blue=0, hex_string='#CD6600', color_blind=None),
                       Color(name='darkorange4', red=139, green=69, blue=0, hex_string='#8B4500', color_blind=None),
                       Color(name='darkorchid', red=153, green=50, blue=204, hex_string='#9932CC', color_blind=None),
                       Color(name='darkorchid1', red=191, green=62, blue=255, hex_string='#BF3EFF', color_blind=None),
                       Color(name='darkorchid2', red=178, green=58, blue=238, hex_string='#B23AEE', color_blind=None),
                       Color(name='darkorchid3', red=154, green=50, blue=205, hex_string='#9A32CD', color_blind=None),
                       Color(name='darkorchid4', red=104, green=34, blue=139, hex_string='#68228B', color_blind=None),
                       Color(name='darksalmon', red=233, green=150, blue=122, hex_string='#E9967A', color_blind=None),
                       Color(name='darkseagreen', red=143, green=188, blue=143, hex_string='#8FBC8F', color_blind=None),
                       Color(name='darkseagreen1', red=193, green=255, blue=193, hex_string='#C1FFC1',
                             color_blind=None),
                       Color(name='darkseagreen2', red=180, green=238, blue=180, hex_string='#B4EEB4',
                             color_blind=None),
                       Color(name='darkseagreen3', red=155, green=205, blue=155, hex_string='#9BCD9B',
                             color_blind=None),
                       Color(name='darkseagreen4', red=105, green=139, blue=105, hex_string='#698B69',
                             color_blind=None),
                       Color(name='darkslateblue', red=72, green=61, blue=139, hex_string='#483D8B', color_blind=None),
                       Color(name='darkslategray', red=47, green=79, blue=79, hex_string='#2F4F4F', color_blind=None),
                       Color(name='darkslategray1', red=151, green=255, blue=255, hex_string='#97FFFF',
                             color_blind=None),
                       Color(name='darkslategray2', red=141, green=238, blue=238, hex_string='#8DEEEE',
                             color_blind=None),
                       Color(name='darkslategray3', red=121, green=205, blue=205, hex_string='#79CDCD',
                             color_blind=None),
                       Color(name='darkslategray4', red=82, green=139, blue=139, hex_string='#528B8B',
                             color_blind=None),
                       Color(name='darkturquoise', red=0, green=206, blue=209, hex_string='#00CED1', color_blind=None),
                       Color(name='darkviolet', red=148, green=0, blue=211, hex_string='#9400D3', color_blind=None),
                       Color(name='deeppink1', red=255, green=20, blue=147, hex_string='#FF1493', color_blind=None),
                       Color(name='deeppink2', red=238, green=18, blue=137, hex_string='#EE1289', color_blind=None),
                       Color(name='deeppink3', red=205, green=16, blue=118, hex_string='#CD1076', color_blind=None),
                       Color(name='deeppink4', red=139, green=10, blue=80, hex_string='#8B0A50', color_blind=None),
                       Color(name='deepskyblue1', red=0, green=191, blue=255, hex_string='#00BFFF', color_blind=None),
                       Color(name='deepskyblue2', red=0, green=178, blue=238, hex_string='#00B2EE', color_blind=None),
                       Color(name='deepskyblue3', red=0, green=154, blue=205, hex_string='#009ACD', color_blind=None),
                       Color(name='deepskyblue4', red=0, green=104, blue=139, hex_string='#00688B', color_blind=None),
                       Color(name='dimgray', red=105, green=105, blue=105, hex_string='#696969', color_blind=None),
                       Color(name='dodgerblue1', red=30, green=144, blue=255, hex_string='#1E90FF', color_blind=None),
                       Color(name='dodgerblue2', red=28, green=134, blue=238, hex_string='#1C86EE', color_blind=None),
                       Color(name='dodgerblue3', red=24, green=116, blue=205, hex_string='#1874CD', color_blind=None),
                       Color(name='dodgerblue4', red=16, green=78, blue=139, hex_string='#104E8B', color_blind=None),
                       Color(name='eggshell', red=252, green=230, blue=201, hex_string='#FCE6C9', color_blind=None),
                       Color(name='emeraldgreen', red=0, green=201, blue=87, hex_string='#00C957', color_blind=None),
                       Color(name='firebrick', red=178, green=34, blue=34, hex_string='#B22222', color_blind=None),
                       Color(name='firebrick1', red=255, green=48, blue=48, hex_string='#FF3030', color_blind=None),
                       Color(name='firebrick2', red=238, green=44, blue=44, hex_string='#EE2C2C', color_blind=None),
                       Color(name='firebrick3', red=205, green=38, blue=38, hex_string='#CD2626', color_blind=None),
                       Color(name='firebrick4', red=139, green=26, blue=26, hex_string='#8B1A1A', color_blind=None),
                       Color(name='flesh', red=255, green=125, blue=64, hex_string='#FF7D40', color_blind=None),
                       Color(name='floralwhite', red=255, green=250, blue=240, hex_string='#FFFAF0', color_blind=None),
                       Color(name='forestgreen', red=34, green=139, blue=34, hex_string='#228B22', color_blind=None),
                       Color(name='gainsboro', red=220, green=220, blue=220, hex_string='#DCDCDC', color_blind=None),
                       Color(name='ghostwhite', red=248, green=248, blue=255, hex_string='#F8F8FF', color_blind=None),
                       Color(name='gold1', red=255, green=215, blue=0, hex_string='#FFD700', color_blind=None),
                       Color(name='gold2', red=238, green=201, blue=0, hex_string='#EEC900', color_blind=None),
                       Color(name='gold3', red=205, green=173, blue=0, hex_string='#CDAD00', color_blind=None),
                       Color(name='gold4', red=139, green=117, blue=0, hex_string='#8B7500', color_blind=None),
                       Color(name='goldenrod', red=218, green=165, blue=32, hex_string='#DAA520', color_blind=None),
                       Color(name='goldenrod1', red=255, green=193, blue=37, hex_string='#FFC125', color_blind=None),
                       Color(name='goldenrod2', red=238, green=180, blue=34, hex_string='#EEB422', color_blind=None),
                       Color(name='goldenrod3', red=205, green=155, blue=29, hex_string='#CD9B1D', color_blind=None),
                       Color(name='goldenrod4', red=139, green=105, blue=20, hex_string='#8B6914', color_blind=None),
                       Color(name='gray', red=128, green=128, blue=128, hex_string='#808080', color_blind=None),
                       Color(name='gray1', red=3, green=3, blue=3, hex_string='#030303', color_blind=None),
                       Color(name='gray10', red=26, green=26, blue=26, hex_string='#1A1A1A', color_blind=None),
                       Color(name='gray11', red=28, green=28, blue=28, hex_string='#1C1C1C', color_blind=None),
                       Color(name='gray12', red=31, green=31, blue=31, hex_string='#1F1F1F', color_blind=None),
                       Color(name='gray13', red=33, green=33, blue=33, hex_string='#212121', color_blind=None),
                       Color(name='gray14', red=36, green=36, blue=36, hex_string='#242424', color_blind=None),
                       Color(name='gray15', red=38, green=38, blue=38, hex_string='#262626', color_blind=None),
                       Color(name='gray16', red=41, green=41, blue=41, hex_string='#292929', color_blind=None),
                       Color(name='gray17', red=43, green=43, blue=43, hex_string='#2B2B2B', color_blind=None),
                       Color(name='gray18', red=46, green=46, blue=46, hex_string='#2E2E2E', color_blind=None),
                       Color(name='gray19', red=48, green=48, blue=48, hex_string='#303030', color_blind=None),
                       Color(name='gray2', red=5, green=5, blue=5, hex_string='#050505', color_blind=None),
                       Color(name='gray20', red=51, green=51, blue=51, hex_string='#333333', color_blind=None),
                       Color(name='gray21', red=54, green=54, blue=54, hex_string='#363636', color_blind=None),
                       Color(name='gray22', red=56, green=56, blue=56, hex_string='#383838', color_blind=None),
                       Color(name='gray23', red=59, green=59, blue=59, hex_string='#3B3B3B', color_blind=None),
                       Color(name='gray24', red=61, green=61, blue=61, hex_string='#3D3D3D', color_blind=None),
                       Color(name='gray25', red=64, green=64, blue=64, hex_string='#404040', color_blind=None),
                       Color(name='gray26', red=66, green=66, blue=66, hex_string='#424242', color_blind=None),
                       Color(name='gray27', red=69, green=69, blue=69, hex_string='#454545', color_blind=None),
                       Color(name='gray28', red=71, green=71, blue=71, hex_string='#474747', color_blind=None),
                       Color(name='gray29', red=74, green=74, blue=74, hex_string='#4A4A4A', color_blind=None),
                       Color(name='gray3', red=8, green=8, blue=8, hex_string='#080808', color_blind=None),
                       Color(name='gray30', red=77, green=77, blue=77, hex_string='#4D4D4D', color_blind=None),
                       Color(name='gray31', red=79, green=79, blue=79, hex_string='#4F4F4F', color_blind=None),
                       Color(name='gray32', red=82, green=82, blue=82, hex_string='#525252', color_blind=None),
                       Color(name='gray33', red=84, green=84, blue=84, hex_string='#545454', color_blind=None),
                       Color(name='gray34', red=87, green=87, blue=87, hex_string='#575757', color_blind=None),
                       Color(name='gray35', red=89, green=89, blue=89, hex_string='#595959', color_blind=None),
                       Color(name='gray36', red=92, green=92, blue=92, hex_string='#5C5C5C', color_blind=None),
                       Color(name='gray37', red=94, green=94, blue=94, hex_string='#5E5E5E', color_blind=None),
                       Color(name='gray38', red=97, green=97, blue=97, hex_string='#616161', color_blind=None),
                       Color(name='gray39', red=99, green=99, blue=99, hex_string='#636363', color_blind=None),
                       Color(name='gray4', red=10, green=10, blue=10, hex_string='#0A0A0A', color_blind=None),
                       Color(name='gray40', red=102, green=102, blue=102, hex_string='#666666', color_blind=None),
                       Color(name='gray42', red=107, green=107, blue=107, hex_string='#6B6B6B', color_blind=None),
                       Color(name='gray43', red=110, green=110, blue=110, hex_string='#6E6E6E', color_blind=None),
                       Color(name='gray44', red=112, green=112, blue=112, hex_string='#707070', color_blind=None),
                       Color(name='gray45', red=115, green=115, blue=115, hex_string='#737373', color_blind=None),
                       Color(name='gray46', red=117, green=117, blue=117, hex_string='#757575', color_blind=None),
                       Color(name='gray47', red=120, green=120, blue=120, hex_string='#787878', color_blind=None),
                       Color(name='gray48', red=122, green=122, blue=122, hex_string='#7A7A7A', color_blind=None),
                       Color(name='gray49', red=125, green=125, blue=125, hex_string='#7D7D7D', color_blind=None),
                       Color(name='gray5', red=13, green=13, blue=13, hex_string='#0D0D0D', color_blind=None),
                       Color(name='gray50', red=127, green=127, blue=127, hex_string='#7F7F7F', color_blind=None),
                       Color(name='gray51', red=130, green=130, blue=130, hex_string='#828282', color_blind=None),
                       Color(name='gray52', red=133, green=133, blue=133, hex_string='#858585', color_blind=None),
                       Color(name='gray53', red=135, green=135, blue=135, hex_string='#878787', color_blind=None),
                       Color(name='gray54', red=138, green=138, blue=138, hex_string='#8A8A8A', color_blind=None),
                       Color(name='gray55', red=140, green=140, blue=140, hex_string='#8C8C8C', color_blind=None),
                       Color(name='gray56', red=143, green=143, blue=143, hex_string='#8F8F8F', color_blind=None),
                       Color(name='gray57', red=145, green=145, blue=145, hex_string='#919191', color_blind=None),
                       Color(name='gray58', red=148, green=148, blue=148, hex_string='#949494', color_blind=None),
                       Color(name='gray59', red=150, green=150, blue=150, hex_string='#969696', color_blind=None),
                       Color(name='gray6', red=15, green=15, blue=15, hex_string='#0F0F0F', color_blind=None),
                       Color(name='gray60', red=153, green=153, blue=153, hex_string='#999999', color_blind=None),
                       Color(name='gray61', red=156, green=156, blue=156, hex_string='#9C9C9C', color_blind=None),
                       Color(name='gray62', red=158, green=158, blue=158, hex_string='#9E9E9E', color_blind=None),
                       Color(name='gray63', red=161, green=161, blue=161, hex_string='#A1A1A1', color_blind=None),
                       Color(name='gray64', red=163, green=163, blue=163, hex_string='#A3A3A3', color_blind=None),
                       Color(name='gray65', red=166, green=166, blue=166, hex_string='#A6A6A6', color_blind=None),
                       Color(name='gray66', red=168, green=168, blue=168, hex_string='#A8A8A8', color_blind=None),
                       Color(name='gray67', red=171, green=171, blue=171, hex_string='#ABABAB', color_blind=None),
                       Color(name='gray68', red=173, green=173, blue=173, hex_string='#ADADAD', color_blind=None),
                       Color(name='gray69', red=176, green=176, blue=176, hex_string='#B0B0B0', color_blind=None),
                       Color(name='gray7', red=18, green=18, blue=18, hex_string='#121212', color_blind=None),
                       Color(name='gray70', red=179, green=179, blue=179, hex_string='#B3B3B3', color_blind=None),
                       Color(name='gray71', red=181, green=181, blue=181, hex_string='#B5B5B5', color_blind=None),
                       Color(name='gray72', red=184, green=184, blue=184, hex_string='#B8B8B8', color_blind=None),
                       Color(name='gray73', red=186, green=186, blue=186, hex_string='#BABABA', color_blind=None),
                       Color(name='gray74', red=189, green=189, blue=189, hex_string='#BDBDBD', color_blind=None),
                       Color(name='gray75', red=191, green=191, blue=191, hex_string='#BFBFBF', color_blind=None),
                       Color(name='gray76', red=194, green=194, blue=194, hex_string='#C2C2C2', color_blind=None),
                       Color(name='gray77', red=196, green=196, blue=196, hex_string='#C4C4C4', color_blind=None),
                       Color(name='gray78', red=199, green=199, blue=199, hex_string='#C7C7C7', color_blind=None),
                       Color(name='gray79', red=201, green=201, blue=201, hex_string='#C9C9C9', color_blind=None),
                       Color(name='gray8', red=20, green=20, blue=20, hex_string='#141414', color_blind=None),
                       Color(name='gray80', red=204, green=204, blue=204, hex_string='#CCCCCC', color_blind=None),
                       Color(name='gray81', red=207, green=207, blue=207, hex_string='#CFCFCF', color_blind=None),
                       Color(name='gray82', red=209, green=209, blue=209, hex_string='#D1D1D1', color_blind=None),
                       Color(name='gray83', red=212, green=212, blue=212, hex_string='#D4D4D4', color_blind=None),
                       Color(name='gray84', red=214, green=214, blue=214, hex_string='#D6D6D6', color_blind=None),
                       Color(name='gray85', red=217, green=217, blue=217, hex_string='#D9D9D9', color_blind=None),
                       Color(name='gray86', red=219, green=219, blue=219, hex_string='#DBDBDB', color_blind=None),
                       Color(name='gray87', red=222, green=222, blue=222, hex_string='#DEDEDE', color_blind=None),
                       Color(name='gray88', red=224, green=224, blue=224, hex_string='#E0E0E0', color_blind=None),
                       Color(name='gray89', red=227, green=227, blue=227, hex_string='#E3E3E3', color_blind=None),
                       Color(name='gray9', red=23, green=23, blue=23, hex_string='#171717', color_blind=None),
                       Color(name='gray90', red=229, green=229, blue=229, hex_string='#E5E5E5', color_blind=None),
                       Color(name='gray91', red=232, green=232, blue=232, hex_string='#E8E8E8', color_blind=None),
                       Color(name='gray92', red=235, green=235, blue=235, hex_string='#EBEBEB', color_blind=None),
                       Color(name='gray93', red=237, green=237, blue=237, hex_string='#EDEDED', color_blind=None),
                       Color(name='gray94', red=240, green=240, blue=240, hex_string='#F0F0F0', color_blind=None),
                       Color(name='gray95', red=242, green=242, blue=242, hex_string='#F2F2F2', color_blind=None),
                       Color(name='gray97', red=247, green=247, blue=247, hex_string='#F7F7F7', color_blind=None),
                       Color(name='gray98', red=250, green=250, blue=250, hex_string='#FAFAFA', color_blind=None),
                       Color(name='gray99', red=252, green=252, blue=252, hex_string='#FCFCFC', color_blind=None),
                       Color(name='green', red=0, green=128, blue=0, hex_string='#008000', color_blind=None),
                       Color(name='green1', red=0, green=255, blue=0, hex_string='#00FF00', color_blind=None),
                       Color(name='green2', red=0, green=238, blue=0, hex_string='#00EE00', color_blind=None),
                       Color(name='green3', red=0, green=205, blue=0, hex_string='#00CD00', color_blind=None),
                       Color(name='green4', red=0, green=139, blue=0, hex_string='#008B00', color_blind=None),
                       Color(name='greenyellow', red=173, green=255, blue=47, hex_string='#ADFF2F', color_blind=None),
                       Color(name='honeydew1', red=240, green=255, blue=240, hex_string='#F0FFF0', color_blind=None),
                       Color(name='honeydew2', red=224, green=238, blue=224, hex_string='#E0EEE0', color_blind=None),
                       Color(name='honeydew3', red=193, green=205, blue=193, hex_string='#C1CDC1', color_blind=None),
                       Color(name='honeydew4', red=131, green=139, blue=131, hex_string='#838B83', color_blind=None),
                       Color(name='hotpink', red=255, green=105, blue=180, hex_string='#FF69B4', color_blind=None),
                       Color(name='hotpink1', red=255, green=110, blue=180, hex_string='#FF6EB4', color_blind=None),
                       Color(name='hotpink2', red=238, green=106, blue=167, hex_string='#EE6AA7', color_blind=None),
                       Color(name='hotpink3', red=205, green=96, blue=144, hex_string='#CD6090', color_blind=None),
                       Color(name='hotpink4', red=139, green=58, blue=98, hex_string='#8B3A62', color_blind=None),
                       Color(name='indianred', red=205, green=92, blue=92, hex_string='#CD5C5C', color_blind=None),
                       Color(name='indianred1', red=255, green=106, blue=106, hex_string='#FF6A6A', color_blind=None),
                       Color(name='indianred2', red=238, green=99, blue=99, hex_string='#EE6363', color_blind=None),
                       Color(name='indianred3', red=205, green=85, blue=85, hex_string='#CD5555', color_blind=None),
                       Color(name='indianred4', red=139, green=58, blue=58, hex_string='#8B3A3A', color_blind=None),
                       Color(name='indigo', red=75, green=0, blue=130, hex_string='#4B0082', color_blind=None),
                       Color(name='ivory1', red=255, green=255, blue=240, hex_string='#FFFFF0', color_blind=None),
                       Color(name='ivory2', red=238, green=238, blue=224, hex_string='#EEEEE0', color_blind=None),
                       Color(name='ivory3', red=205, green=205, blue=193, hex_string='#CDCDC1', color_blind=None),
                       Color(name='ivory4', red=139, green=139, blue=131, hex_string='#8B8B83', color_blind=None),
                       Color(name='ivoryblack', red=41, green=36, blue=33, hex_string='#292421', color_blind=None),
                       Color(name='khaki', red=240, green=230, blue=140, hex_string='#F0E68C', color_blind=None),
                       Color(name='khaki1', red=255, green=246, blue=143, hex_string='#FFF68F', color_blind=None),
                       Color(name='khaki2', red=238, green=230, blue=133, hex_string='#EEE685', color_blind=None),
                       Color(name='khaki3', red=205, green=198, blue=115, hex_string='#CDC673', color_blind=None),
                       Color(name='khaki4', red=139, green=134, blue=78, hex_string='#8B864E', color_blind=None),
                       Color(name='lavender', red=230, green=230, blue=250, hex_string='#E6E6FA', color_blind=None),
                       Color(name='lavenderblush1', red=255, green=240, blue=245, hex_string='#FFF0F5',
                             color_blind=None),
                       Color(name='lavenderblush2', red=238, green=224, blue=229, hex_string='#EEE0E5',
                             color_blind=None),
                       Color(name='lavenderblush3', red=205, green=193, blue=197, hex_string='#CDC1C5',
                             color_blind=None),
                       Color(name='lavenderblush4', red=139, green=131, blue=134, hex_string='#8B8386',
                             color_blind=None),
                       Color(name='lawngreen', red=124, green=252, blue=0, hex_string='#7CFC00', color_blind=None),
                       Color(name='lemonchiffon1', red=255, green=250, blue=205, hex_string='#FFFACD',
                             color_blind=None),
                       Color(name='lemonchiffon2', red=238, green=233, blue=191, hex_string='#EEE9BF',
                             color_blind=None),
                       Color(name='lemonchiffon3', red=205, green=201, blue=165, hex_string='#CDC9A5',
                             color_blind=None),
                       Color(name='lemonchiffon4', red=139, green=137, blue=112, hex_string='#8B8970',
                             color_blind=None),
                       Color(name='lightblue', red=173, green=216, blue=230, hex_string='#ADD8E6', color_blind=None),
                       Color(name='lightblue1', red=191, green=239, blue=255, hex_string='#BFEFFF', color_blind=None),
                       Color(name='lightblue2', red=178, green=223, blue=238, hex_string='#B2DFEE', color_blind=None),
                       Color(name='lightblue3', red=154, green=192, blue=205, hex_string='#9AC0CD', color_blind=None),
                       Color(name='lightblue4', red=104, green=131, blue=139, hex_string='#68838B', color_blind=None),
                       Color(name='lightcoral', red=240, green=128, blue=128, hex_string='#F08080', color_blind=None),
                       Color(name='lightcyan1', red=224, green=255, blue=255, hex_string='#E0FFFF', color_blind=None),
                       Color(name='lightcyan2', red=209, green=238, blue=238, hex_string='#D1EEEE', color_blind=None),
                       Color(name='lightcyan3', red=180, green=205, blue=205, hex_string='#B4CDCD', color_blind=None),
                       Color(name='lightcyan4', red=122, green=139, blue=139, hex_string='#7A8B8B', color_blind=None),
                       Color(name='lightgoldenrod1', red=255, green=236, blue=139, hex_string='#FFEC8B',
                             color_blind=None),
                       Color(name='lightgoldenrod2', red=238, green=220, blue=130, hex_string='#EEDC82',
                             color_blind=None),
                       Color(name='lightgoldenrod3', red=205, green=190, blue=112, hex_string='#CDBE70',
                             color_blind=None),
                       Color(name='lightgoldenrod4', red=139, green=129, blue=76, hex_string='#8B814C',
                             color_blind=None),
                       Color(name='lightgoldenrodyellow', red=250, green=250, blue=210, hex_string='#FAFAD2',
                             color_blind=None),
                       Color(name='lightgrey', red=211, green=211, blue=211, hex_string='#D3D3D3', color_blind=None),
                       Color(name='lightpink', red=255, green=182, blue=193, hex_string='#FFB6C1', color_blind=None),
                       Color(name='lightpink1', red=255, green=174, blue=185, hex_string='#FFAEB9', color_blind=None),
                       Color(name='lightpink2', red=238, green=162, blue=173, hex_string='#EEA2AD', color_blind=None),
                       Color(name='lightpink3', red=205, green=140, blue=149, hex_string='#CD8C95', color_blind=None),
                       Color(name='lightpink4', red=139, green=95, blue=101, hex_string='#8B5F65', color_blind=None),
                       Color(name='lightsalmon1', red=255, green=160, blue=122, hex_string='#FFA07A', color_blind=None),
                       Color(name='lightsalmon2', red=238, green=149, blue=114, hex_string='#EE9572', color_blind=None),
                       Color(name='lightsalmon3', red=205, green=129, blue=98, hex_string='#CD8162', color_blind=None),
                       Color(name='lightsalmon4', red=139, green=87, blue=66, hex_string='#8B5742', color_blind=None),
                       Color(name='lightseagreen', red=32, green=178, blue=170, hex_string='#20B2AA', color_blind=None),
                       Color(name='lightskyblue', red=135, green=206, blue=250, hex_string='#87CEFA', color_blind=None),
                       Color(name='lightskyblue1', red=176, green=226, blue=255, hex_string='#B0E2FF',
                             color_blind=None),
                       Color(name='lightskyblue2', red=164, green=211, blue=238, hex_string='#A4D3EE',
                             color_blind=None),
                       Color(name='lightskyblue3', red=141, green=182, blue=205, hex_string='#8DB6CD',
                             color_blind=None),
                       Color(name='lightskyblue4', red=96, green=123, blue=139, hex_string='#607B8B', color_blind=None),
                       Color(name='lightslateblue', red=132, green=112, blue=255, hex_string='#8470FF',
                             color_blind=None),
                       Color(name='lightslategray', red=119, green=136, blue=153, hex_string='#778899',
                             color_blind=None),
                       Color(name='lightsteelblue', red=176, green=196, blue=222, hex_string='#B0C4DE',
                             color_blind=None),
                       Color(name='lightsteelblue1', red=202, green=225, blue=255, hex_string='#CAE1FF',
                             color_blind=None),
                       Color(name='lightsteelblue2', red=188, green=210, blue=238, hex_string='#BCD2EE',
                             color_blind=None),
                       Color(name='lightsteelblue3', red=162, green=181, blue=205, hex_string='#A2B5CD',
                             color_blind=None),
                       Color(name='lightsteelblue4', red=110, green=123, blue=139, hex_string='#6E7B8B',
                             color_blind=None),
                       Color(name='lightyellow1', red=255, green=255, blue=224, hex_string='#FFFFE0', color_blind=None),
                       Color(name='lightyellow2', red=238, green=238, blue=209, hex_string='#EEEED1', color_blind=None),
                       Color(name='lightyellow3', red=205, green=205, blue=180, hex_string='#CDCDB4', color_blind=None),
                       Color(name='lightyellow4', red=139, green=139, blue=122, hex_string='#8B8B7A', color_blind=None),
                       Color(name='limegreen', red=50, green=205, blue=50, hex_string='#32CD32', color_blind=None),
                       Color(name='linen', red=250, green=240, blue=230, hex_string='#FAF0E6', color_blind=None),
                       Color(name='magenta', red=255, green=0, blue=255, hex_string='#FF00FF', color_blind=None),
                       Color(name='magenta2', red=238, green=0, blue=238, hex_string='#EE00EE', color_blind=None),
                       Color(name='magenta3', red=205, green=0, blue=205, hex_string='#CD00CD', color_blind=None),
                       Color(name='magenta4', red=139, green=0, blue=139, hex_string='#8B008B', color_blind=None),
                       Color(name='manganeseblue', red=3, green=168, blue=158, hex_string='#03A89E', color_blind=None),
                       Color(name='maroon', red=128, green=0, blue=0, hex_string='#800000', color_blind=None),
                       Color(name='maroon1', red=255, green=52, blue=179, hex_string='#FF34B3', color_blind=None),
                       Color(name='maroon2', red=238, green=48, blue=167, hex_string='#EE30A7', color_blind=None),
                       Color(name='maroon3', red=205, green=41, blue=144, hex_string='#CD2990', color_blind=None),
                       Color(name='maroon4', red=139, green=28, blue=98, hex_string='#8B1C62', color_blind=None),
                       Color(name='mediumorchid', red=186, green=85, blue=211, hex_string='#BA55D3', color_blind=None),
                       Color(name='mediumorchid1', red=224, green=102, blue=255, hex_string='#E066FF',
                             color_blind=None),
                       Color(name='mediumorchid2', red=209, green=95, blue=238, hex_string='#D15FEE', color_blind=None),
                       Color(name='mediumorchid3', red=180, green=82, blue=205, hex_string='#B452CD', color_blind=None),
                       Color(name='mediumorchid4', red=122, green=55, blue=139, hex_string='#7A378B', color_blind=None),
                       Color(name='mediumpurple', red=147, green=112, blue=219, hex_string='#9370DB', color_blind=None),
                       Color(name='mediumpurple1', red=171, green=130, blue=255, hex_string='#AB82FF',
                             color_blind=None),
                       Color(name='mediumpurple2', red=159, green=121, blue=238, hex_string='#9F79EE',
                             color_blind=None),
                       Color(name='mediumpurple3', red=137, green=104, blue=205, hex_string='#8968CD',
                             color_blind=None),
                       Color(name='mediumpurple4', red=93, green=71, blue=139, hex_string='#5D478B', color_blind=None),
                       Color(name='mediumseagreen', red=60, green=179, blue=113, hex_string='#3CB371',
                             color_blind=None),
                       Color(name='mediumslateblue', red=123, green=104, blue=238, hex_string='#7B68EE',
                             color_blind=None),
                       Color(name='mediumspringgreen', red=0, green=250, blue=154, hex_string='#00FA9A',
                             color_blind=None),
                       Color(name='mediumturquoise', red=72, green=209, blue=204, hex_string='#48D1CC',
                             color_blind=None),
                       Color(name='mediumvioletred', red=199, green=21, blue=133, hex_string='#C71585',
                             color_blind=None),
                       Color(name='melon', red=227, green=168, blue=105, hex_string='#E3A869', color_blind=None),
                       Color(name='midnightblue', red=25, green=25, blue=112, hex_string='#191970', color_blind=None),
                       Color(name='mint', red=189, green=252, blue=201, hex_string='#BDFCC9', color_blind=None),
                       Color(name='mintcream', red=245, green=255, blue=250, hex_string='#F5FFFA', color_blind=None),
                       Color(name='mistyrose1', red=255, green=228, blue=225, hex_string='#FFE4E1', color_blind=None),
                       Color(name='mistyrose2', red=238, green=213, blue=210, hex_string='#EED5D2', color_blind=None),
                       Color(name='mistyrose3', red=205, green=183, blue=181, hex_string='#CDB7B5', color_blind=None),
                       Color(name='mistyrose4', red=139, green=125, blue=123, hex_string='#8B7D7B', color_blind=None),
                       Color(name='moccasin', red=255, green=228, blue=181, hex_string='#FFE4B5', color_blind=None),
                       Color(name='navajowhite1', red=255, green=222, blue=173, hex_string='#FFDEAD', color_blind=None),
                       Color(name='navajowhite2', red=238, green=207, blue=161, hex_string='#EECFA1', color_blind=None),
                       Color(name='navajowhite3', red=205, green=179, blue=139, hex_string='#CDB38B', color_blind=None),
                       Color(name='navajowhite4', red=139, green=121, blue=94, hex_string='#8B795E', color_blind=None),
                       Color(name='navy', red=0, green=0, blue=128, hex_string='#000080', color_blind=None),
                       Color(name='oldlace', red=253, green=245, blue=230, hex_string='#FDF5E6', color_blind=None),
                       Color(name='olive', red=128, green=128, blue=0, hex_string='#808000', color_blind=None),
                       Color(name='olivedrab', red=107, green=142, blue=35, hex_string='#6B8E23', color_blind=None),
                       Color(name='olivedrab1', red=192, green=255, blue=62, hex_string='#C0FF3E', color_blind=None),
                       Color(name='olivedrab2', red=179, green=238, blue=58, hex_string='#B3EE3A', color_blind=None),
                       Color(name='olivedrab3', red=154, green=205, blue=50, hex_string='#9ACD32', color_blind=None),
                       Color(name='olivedrab4', red=105, green=139, blue=34, hex_string='#698B22', color_blind=None),
                       Color(name='orange', red=255, green=128, blue=0, hex_string='#FF8000', color_blind=None),
                       Color(name='orange1', red=255, green=165, blue=0, hex_string='#FFA500', color_blind=None),
                       Color(name='orange2', red=238, green=154, blue=0, hex_string='#EE9A00', color_blind=None),
                       Color(name='orange3', red=205, green=133, blue=0, hex_string='#CD8500', color_blind=None),
                       Color(name='orange4', red=139, green=90, blue=0, hex_string='#8B5A00', color_blind=None),
                       Color(name='orangered1', red=255, green=69, blue=0, hex_string='#FF4500', color_blind=None),
                       Color(name='orangered2', red=238, green=64, blue=0, hex_string='#EE4000', color_blind=None),
                       Color(name='orangered3', red=205, green=55, blue=0, hex_string='#CD3700', color_blind=None),
                       Color(name='orangered4', red=139, green=37, blue=0, hex_string='#8B2500', color_blind=None),
                       Color(name='orchid', red=218, green=112, blue=214, hex_string='#DA70D6', color_blind=None),
                       Color(name='orchid1', red=255, green=131, blue=250, hex_string='#FF83FA', color_blind=None),
                       Color(name='orchid2', red=238, green=122, blue=233, hex_string='#EE7AE9', color_blind=None),
                       Color(name='orchid3', red=205, green=105, blue=201, hex_string='#CD69C9', color_blind=None),
                       Color(name='orchid4', red=139, green=71, blue=137, hex_string='#8B4789', color_blind=None),
                       Color(name='palegoldenrod', red=238, green=232, blue=170, hex_string='#EEE8AA',
                             color_blind=None),
                       Color(name='palegreen', red=152, green=251, blue=152, hex_string='#98FB98', color_blind=None),
                       Color(name='palegreen1', red=154, green=255, blue=154, hex_string='#9AFF9A', color_blind=None),
                       Color(name='palegreen2', red=144, green=238, blue=144, hex_string='#90EE90', color_blind=None),
                       Color(name='palegreen3', red=124, green=205, blue=124, hex_string='#7CCD7C', color_blind=None),
                       Color(name='palegreen4', red=84, green=139, blue=84, hex_string='#548B54', color_blind=None),
                       Color(name='paleturquoise1', red=187, green=255, blue=255, hex_string='#BBFFFF',
                             color_blind=None),
                       Color(name='paleturquoise2', red=174, green=238, blue=238, hex_string='#AEEEEE',
                             color_blind=None),
                       Color(name='paleturquoise3', red=150, green=205, blue=205, hex_string='#96CDCD',
                             color_blind=None),
                       Color(name='paleturquoise4', red=102, green=139, blue=139, hex_string='#668B8B',
                             color_blind=None),
                       Color(name='palevioletred', red=219, green=112, blue=147, hex_string='#DB7093',
                             color_blind=None),
                       Color(name='palevioletred1', red=255, green=130, blue=171, hex_string='#FF82AB',
                             color_blind=None),
                       Color(name='palevioletred2', red=238, green=121, blue=159, hex_string='#EE799F',
                             color_blind=None),
                       Color(name='palevioletred3', red=205, green=104, blue=137, hex_string='#CD6889',
                             color_blind=None),
                       Color(name='palevioletred4', red=139, green=71, blue=93, hex_string='#8B475D', color_blind=None),
                       Color(name='papayawhip', red=255, green=239, blue=213, hex_string='#FFEFD5', color_blind=None),
                       Color(name='peachpuff1', red=255, green=218, blue=185, hex_string='#FFDAB9', color_blind=None),
                       Color(name='peachpuff2', red=238, green=203, blue=173, hex_string='#EECBAD', color_blind=None),
                       Color(name='peachpuff3', red=205, green=175, blue=149, hex_string='#CDAF95', color_blind=None),
                       Color(name='peachpuff4', red=139, green=119, blue=101, hex_string='#8B7765', color_blind=None),
                       Color(name='peacock', red=51, green=161, blue=201, hex_string='#33A1C9', color_blind=None),
                       Color(name='pink', red=255, green=192, blue=203, hex_string='#FFC0CB', color_blind=None),
                       Color(name='pink1', red=255, green=181, blue=197, hex_string='#FFB5C5', color_blind=None),
                       Color(name='pink2', red=238, green=169, blue=184, hex_string='#EEA9B8', color_blind=None),
                       Color(name='pink3', red=205, green=145, blue=158, hex_string='#CD919E', color_blind=None),
                       Color(name='pink4', red=139, green=99, blue=108, hex_string='#8B636C', color_blind=None),
                       Color(name='plum', red=221, green=160, blue=221, hex_string='#DDA0DD', color_blind=None),
                       Color(name='plum1', red=255, green=187, blue=255, hex_string='#FFBBFF', color_blind=None),
                       Color(name='plum2', red=238, green=174, blue=238, hex_string='#EEAEEE', color_blind=None),
                       Color(name='plum3', red=205, green=150, blue=205, hex_string='#CD96CD', color_blind=None),
                       Color(name='plum4', red=139, green=102, blue=139, hex_string='#8B668B', color_blind=None),
                       Color(name='powderblue', red=176, green=224, blue=230, hex_string='#B0E0E6', color_blind=None),
                       Color(name='purple', red=128, green=0, blue=128, hex_string='#800080', color_blind=None),
                       Color(name='purple1', red=155, green=48, blue=255, hex_string='#9B30FF', color_blind=None),
                       Color(name='purple2', red=145, green=44, blue=238, hex_string='#912CEE', color_blind=None),
                       Color(name='purple3', red=125, green=38, blue=205, hex_string='#7D26CD', color_blind=None),
                       Color(name='purple4', red=85, green=26, blue=139, hex_string='#551A8B', color_blind=None),
                       Color(name='raspberry', red=135, green=38, blue=87, hex_string='#872657', color_blind=None),
                       Color(name='rawsienna', red=199, green=97, blue=20, hex_string='#C76114', color_blind=None),
                       Color(name='red1', red=255, green=0, blue=0, hex_string='#FF0000', color_blind=None),
                       Color(name='red2', red=238, green=0, blue=0, hex_string='#EE0000', color_blind=None),
                       Color(name='red3', red=205, green=0, blue=0, hex_string='#CD0000', color_blind=None),
                       Color(name='red4', red=139, green=0, blue=0, hex_string='#8B0000', color_blind=None),
                       Color(name='rosybrown', red=188, green=143, blue=143, hex_string='#BC8F8F', color_blind=None),
                       Color(name='rosybrown1', red=255, green=193, blue=193, hex_string='#FFC1C1', color_blind=None),
                       Color(name='rosybrown2', red=238, green=180, blue=180, hex_string='#EEB4B4', color_blind=None),
                       Color(name='rosybrown3', red=205, green=155, blue=155, hex_string='#CD9B9B', color_blind=None),
                       Color(name='rosybrown4', red=139, green=105, blue=105, hex_string='#8B6969', color_blind=None),
                       Color(name='royalblue', red=65, green=105, blue=225, hex_string='#4169E1', color_blind=None),
                       Color(name='royalblue1', red=72, green=118, blue=255, hex_string='#4876FF', color_blind=None),
                       Color(name='royalblue2', red=67, green=110, blue=238, hex_string='#436EEE', color_blind=None),
                       Color(name='royalblue3', red=58, green=95, blue=205, hex_string='#3A5FCD', color_blind=None),
                       Color(name='royalblue4', red=39, green=64, blue=139, hex_string='#27408B', color_blind=None),
                       Color(name='salmon', red=250, green=128, blue=114, hex_string='#FA8072', color_blind=None),
                       Color(name='salmon1', red=255, green=140, blue=105, hex_string='#FF8C69', color_blind=None),
                       Color(name='salmon2', red=238, green=130, blue=98, hex_string='#EE8262', color_blind=None),
                       Color(name='salmon3', red=205, green=112, blue=84, hex_string='#CD7054', color_blind=None),
                       Color(name='salmon4', red=139, green=76, blue=57, hex_string='#8B4C39', color_blind=None),
                       Color(name='sandybrown', red=244, green=164, blue=96, hex_string='#F4A460', color_blind=None),
                       Color(name='sapgreen', red=48, green=128, blue=20, hex_string='#308014', color_blind=None),
                       Color(name='seagreen1', red=84, green=255, blue=159, hex_string='#54FF9F', color_blind=None),
                       Color(name='seagreen2', red=78, green=238, blue=148, hex_string='#4EEE94', color_blind=None),
                       Color(name='seagreen3', red=67, green=205, blue=128, hex_string='#43CD80', color_blind=None),
                       Color(name='seagreen4', red=46, green=139, blue=87, hex_string='#2E8B57', color_blind=None),
                       Color(name='seashell1', red=255, green=245, blue=238, hex_string='#FFF5EE', color_blind=None),
                       Color(name='seashell2', red=238, green=229, blue=222, hex_string='#EEE5DE', color_blind=None),
                       Color(name='seashell3', red=205, green=197, blue=191, hex_string='#CDC5BF', color_blind=None),
                       Color(name='seashell4', red=139, green=134, blue=130, hex_string='#8B8682', color_blind=None),
                       Color(name='sepia', red=94, green=38, blue=18, hex_string='#5E2612', color_blind=None),
                       Color(name='sgibeet', red=142, green=56, blue=142, hex_string='#8E388E', color_blind=None),
                       Color(name='sgibrightgray', red=197, green=193, blue=170, hex_string='#C5C1AA',
                             color_blind=None),
                       Color(name='sgichartreuse', red=113, green=198, blue=113, hex_string='#71C671',
                             color_blind=None),
                       Color(name='sgidarkgray', red=85, green=85, blue=85, hex_string='#555555', color_blind=None),
                       Color(name='sgigray12', red=30, green=30, blue=30, hex_string='#1E1E1E', color_blind=None),
                       Color(name='sgigray16', red=40, green=40, blue=40, hex_string='#282828', color_blind=None),
                       Color(name='sgigray32', red=81, green=81, blue=81, hex_string='#515151', color_blind=None),
                       Color(name='sgigray36', red=91, green=91, blue=91, hex_string='#5B5B5B', color_blind=None),
                       Color(name='sgigray52', red=132, green=132, blue=132, hex_string='#848484', color_blind=None),
                       Color(name='sgigray56', red=142, green=142, blue=142, hex_string='#8E8E8E', color_blind=None),
                       Color(name='sgigray72', red=183, green=183, blue=183, hex_string='#B7B7B7', color_blind=None),
                       Color(name='sgigray76', red=193, green=193, blue=193, hex_string='#C1C1C1', color_blind=None),
                       Color(name='sgigray92', red=234, green=234, blue=234, hex_string='#EAEAEA', color_blind=None),
                       Color(name='sgigray96', red=244, green=244, blue=244, hex_string='#F4F4F4', color_blind=None),
                       Color(name='sgilightblue', red=125, green=158, blue=192, hex_string='#7D9EC0', color_blind=None),
                       Color(name='sgilightgray', red=170, green=170, blue=170, hex_string='#AAAAAA', color_blind=None),
                       Color(name='sgiolivedrab', red=142, green=142, blue=56, hex_string='#8E8E38', color_blind=None),
                       Color(name='sgisalmon', red=198, green=113, blue=113, hex_string='#C67171', color_blind=None),
                       Color(name='sgislateblue', red=113, green=113, blue=198, hex_string='#7171C6', color_blind=None),
                       Color(name='sgiteal', red=56, green=142, blue=142, hex_string='#388E8E', color_blind=None),
                       Color(name='sienna', red=160, green=82, blue=45, hex_string='#A0522D', color_blind=None),
                       Color(name='sienna1', red=255, green=130, blue=71, hex_string='#FF8247', color_blind=None),
                       Color(name='sienna2', red=238, green=121, blue=66, hex_string='#EE7942', color_blind=None),
                       Color(name='sienna3', red=205, green=104, blue=57, hex_string='#CD6839', color_blind=None),
                       Color(name='sienna4', red=139, green=71, blue=38, hex_string='#8B4726', color_blind=None),
                       Color(name='silver', red=192, green=192, blue=192, hex_string='#C0C0C0', color_blind=None),
                       Color(name='skyblue', red=135, green=206, blue=235, hex_string='#87CEEB', color_blind=None),
                       Color(name='skyblue1', red=135, green=206, blue=255, hex_string='#87CEFF', color_blind=None),
                       Color(name='skyblue2', red=126, green=192, blue=238, hex_string='#7EC0EE', color_blind=None),
                       Color(name='skyblue3', red=108, green=166, blue=205, hex_string='#6CA6CD', color_blind=None),
                       Color(name='skyblue4', red=74, green=112, blue=139, hex_string='#4A708B', color_blind=None),
                       Color(name='slateblue', red=106, green=90, blue=205, hex_string='#6A5ACD', color_blind=None),
                       Color(name='slateblue1', red=131, green=111, blue=255, hex_string='#836FFF', color_blind=None),
                       Color(name='slateblue2', red=122, green=103, blue=238, hex_string='#7A67EE', color_blind=None),
                       Color(name='slateblue3', red=105, green=89, blue=205, hex_string='#6959CD', color_blind=None),
                       Color(name='slateblue4', red=71, green=60, blue=139, hex_string='#473C8B', color_blind=None),
                       Color(name='slategray', red=112, green=128, blue=144, hex_string='#708090', color_blind=None),
                       Color(name='slategray1', red=198, green=226, blue=255, hex_string='#C6E2FF', color_blind=None),
                       Color(name='slategray2', red=185, green=211, blue=238, hex_string='#B9D3EE', color_blind=None),
                       Color(name='slategray3', red=159, green=182, blue=205, hex_string='#9FB6CD', color_blind=None),
                       Color(name='slategray4', red=108, green=123, blue=139, hex_string='#6C7B8B', color_blind=None),
                       Color(name='snow1', red=255, green=250, blue=250, hex_string='#FFFAFA', color_blind=None),
                       Color(name='snow2', red=238, green=233, blue=233, hex_string='#EEE9E9', color_blind=None),
                       Color(name='snow3', red=205, green=201, blue=201, hex_string='#CDC9C9', color_blind=None),
                       Color(name='snow4', red=139, green=137, blue=137, hex_string='#8B8989', color_blind=None),
                       Color(name='springgreen', red=0, green=255, blue=127, hex_string='#00FF7F', color_blind=None),
                       Color(name='springgreen1', red=0, green=238, blue=118, hex_string='#00EE76', color_blind=None),
                       Color(name='springgreen2', red=0, green=205, blue=102, hex_string='#00CD66', color_blind=None),
                       Color(name='springgreen3', red=0, green=139, blue=69, hex_string='#008B45', color_blind=None),
                       Color(name='steelblue', red=70, green=130, blue=180, hex_string='#4682B4', color_blind=None),
                       Color(name='steelblue1', red=99, green=184, blue=255, hex_string='#63B8FF', color_blind=None),
                       Color(name='steelblue2', red=92, green=172, blue=238, hex_string='#5CACEE', color_blind=None),
                       Color(name='steelblue3', red=79, green=148, blue=205, hex_string='#4F94CD', color_blind=None),
                       Color(name='steelblue4', red=54, green=100, blue=139, hex_string='#36648B', color_blind=None),
                       Color(name='tan', red=210, green=180, blue=140, hex_string='#D2B48C', color_blind=None),
                       Color(name='tan1', red=255, green=165, blue=79, hex_string='#FFA54F', color_blind=None),
                       Color(name='tan2', red=238, green=154, blue=73, hex_string='#EE9A49', color_blind=None),
                       Color(name='tan3', red=205, green=133, blue=63, hex_string='#CD853F', color_blind=None),
                       Color(name='tan4', red=139, green=90, blue=43, hex_string='#8B5A2B', color_blind=None),
                       Color(name='teal', red=0, green=128, blue=128, hex_string='#008080', color_blind=None),
                       Color(name='thistle', red=216, green=191, blue=216, hex_string='#D8BFD8', color_blind=None),
                       Color(name='thistle1', red=255, green=225, blue=255, hex_string='#FFE1FF', color_blind=None),
                       Color(name='thistle2', red=238, green=210, blue=238, hex_string='#EED2EE', color_blind=None),
                       Color(name='thistle3', red=205, green=181, blue=205, hex_string='#CDB5CD', color_blind=None),
                       Color(name='thistle4', red=139, green=123, blue=139, hex_string='#8B7B8B', color_blind=None),
                       Color(name='tomato1', red=255, green=99, blue=71, hex_string='#FF6347', color_blind=None),
                       Color(name='tomato2', red=238, green=92, blue=66, hex_string='#EE5C42', color_blind=None),
                       Color(name='tomato3', red=205, green=79, blue=57, hex_string='#CD4F39', color_blind=None),
                       Color(name='tomato4', red=139, green=54, blue=38, hex_string='#8B3626', color_blind=None),
                       Color(name='turquoise', red=64, green=224, blue=208, hex_string='#40E0D0', color_blind=None),
                       Color(name='turquoise1', red=0, green=245, blue=255, hex_string='#00F5FF', color_blind=None),
                       Color(name='turquoise2', red=0, green=229, blue=238, hex_string='#00E5EE', color_blind=None),
                       Color(name='turquoise3', red=0, green=197, blue=205, hex_string='#00C5CD', color_blind=None),
                       Color(name='turquoise4', red=0, green=134, blue=139, hex_string='#00868B', color_blind=None),
                       Color(name='turquoiseblue', red=0, green=199, blue=140, hex_string='#00C78C', color_blind=None),
                       Color(name='violet', red=238, green=130, blue=238, hex_string='#EE82EE', color_blind=None),
                       Color(name='violetred', red=208, green=32, blue=144, hex_string='#D02090', color_blind=None),
                       Color(name='violetred1', red=255, green=62, blue=150, hex_string='#FF3E96', color_blind=None),
                       Color(name='violetred2', red=238, green=58, blue=140, hex_string='#EE3A8C', color_blind=None),
                       Color(name='violetred3', red=205, green=50, blue=120, hex_string='#CD3278', color_blind=None),
                       Color(name='violetred4', red=139, green=34, blue=82, hex_string='#8B2252', color_blind=None),
                       Color(name='warmgrey', red=128, green=128, blue=105, hex_string='#808069', color_blind=None),
                       Color(name='wheat', red=245, green=222, blue=179, hex_string='#F5DEB3', color_blind=None),
                       Color(name='wheat1', red=255, green=231, blue=186, hex_string='#FFE7BA', color_blind=None),
                       Color(name='wheat2', red=238, green=216, blue=174, hex_string='#EED8AE', color_blind=None),
                       Color(name='wheat3', red=205, green=186, blue=150, hex_string='#CDBA96', color_blind=None),
                       Color(name='wheat4', red=139, green=126, blue=102, hex_string='#8B7E66', color_blind=None),
                       Color(name='white', red=255, green=255, blue=255, hex_string='#FFFFFF', color_blind=None),
                       Color(name='whitesmoke', red=245, green=245, blue=245, hex_string='#F5F5F5', color_blind=None),
                       Color(name='yellow1', red=255, green=255, blue=0, hex_string='#FFFF00', color_blind=None),
                       Color(name='yellow2', red=238, green=238, blue=0, hex_string='#EEEE00', color_blind=None),
                       Color(name='yellow3', red=205, green=205, blue=0, hex_string='#CDCD00', color_blind=None),
                       Color(name='yellow4', red=139, green=139, blue=0, hex_string='#8B8B00', color_blind=None),
                       Color(name='tol1', red=51, green=34, blue=136, hex_string='#332288', color_blind='tol'),
                       Color(name='tol2', red=17, green=119, blue=51, hex_string='#117733', color_blind='tol'),
                       Color(name='tol3', red=68, green=170, blue=153, hex_string='#44AA99', color_blind='tol'),
                       Color(name='tol4', red=136, green=204, blue=238, hex_string='#88CCEE', color_blind='tol'),
                       Color(name='tol5', red=221, green=204, blue=119, hex_string='#DDCC77', color_blind='tol'),
                       Color(name='tol6', red=204, green=102, blue=119, hex_string='#CC6677', color_blind='tol'),
                       Color(name='tol7', red=170, green=68, blue=153, hex_string='#AA4499', color_blind='tol'),
                       Color(name='tol8', red=136, green=34, blue=85, hex_string='#882255', color_blind='tol'),
                       Color(name='ibm1', red=100, green=143, blue=255, hex_string='#648FFF', color_blind='ibm'),
                       Color(name='ibm2', red=120, green=94, blue=240, hex_string='#785EF0', color_blind='ibm'),
                       Color(name='ibm3', red=220, green=38, blue=127, hex_string='#DC267F', color_blind='ibm'),
                       Color(name='ibm4', red=254, green=97, blue=0, hex_string='#FE6100', color_blind='ibm'),
                       Color(name='ibm5', red=255, green=176, blue=0, hex_string='#FFB000', color_blind='ibm'),
                       Color(name='okabe_ito1', red=230, green=159, blue=0, hex_string='#E69F00',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito2', red=86, green=180, blue=233, hex_string='#56B4E9',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito3', red=0, green=158, blue=115, hex_string='#009E73',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito4', red=240, green=228, blue=66, hex_string='#F0E442',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito5', red=0, green=114, blue=178, hex_string='#0072B2',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito6', red=213, green=94, blue=0, hex_string='#D55E00',
                             color_blind='okabe_ito'),
                       Color(name='okabe_ito7', red=204, green=121, blue=167, hex_string='#CC79A7',
                             color_blind='okabe_ito')]

    def search_by_name(self, name: str) -> List[Color]:
        return [item for item in self.colors if item.name == name]

    def search_by_rgb(self, rgb: Tuple[int, int, int]) -> List[Color]:
        return [item for item in self.colors if item.red == rgb[0] and item.green == rgb[1] and item.blue == rgb[2]]

    def search_by_hex_string(self, hex_string: str) -> List[Color]:
        return [item for item in self.colors if item.hex_string == hex_string]

    def search_by_color_blind(self, color_blind_type: str):
        return [item for item in self.colors if item.color_blind == color_blind_type]

    def closest(self, rgb: Tuple[int, int, int]) -> Color:
        """
        import math
        d = {math.dist(list(rgb), (item.red, item.green, item.blue))/255: item for item in self.colors}
        od = collections.OrderedDict(sorted(d.items()))
        return list(od.values())[-1]
        """
        raise NotImplementedError


def draw_molecule(rdmol):
    """
        Produces the data necessary to create a picture of a molecule with RDKit

        :param:
            rdmol: an RDKit Mol object

        :return:
            The data in text format of the picture. It can be converted into a png file using the
            linchemin.IO.io.write_rdkit_depict function
    """
    DrawingOptions.atomLabelFontSize = 55
    DrawingOptions.dotsPerAngstrom = 100
    DrawingOptions.bondLineWidth = 3.0

    d2d = Draw.rdMolDraw2D.MolDraw2DCairo(350, 300)
    draw_rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)
    d2d.DrawMolecule(draw_rdmol)
    return d2d.GetDrawingText()


def draw_reaction(rdrxn):
    """
        Produces the data necessary to create a picture of a molecule with RDKit

        :param:
            rdrxn: an RDKit ChemicalReaction object

        :return:
            The data in text format of the picture. It can be converted into a png file using the
            linchemin.IO.io.write_rdkit_depict function
    """
    DrawingOptions.atomLabelFontSize = 55
    DrawingOptions.dotsPerAngstrom = 100
    DrawingOptions.bondLineWidth = 3.0

    d2d = Draw.MolDraw2DCairo(800, 200)
    d2d.DrawReaction(rdrxn, highlightByReactant=True)
    return d2d.GetDrawingText()


def draw_disconnection(rdmol, reacting_atoms, new_bonds, modified_bonds, show_atom_maps: bool = False):
    Chem.SanitizeMol(rdmol)
    if not show_atom_maps:
        rdmol = cif.remove_rdmol_atom_mapping(rdmol)

    color_new_bonds = 1, 0.4, 0.4
    color_modified_bonds = 0.4, 0.4, 1
    color_reacting_atoms = 0.5, 0.5, 0.6

    d2d = Draw.rdMolDraw2D.MolDraw2DCairo(350, 300)
    d2d.drawOptions().useBWAtomPalette()
    d2d.drawOptions().continuousHighlight = True
    d2d.drawOptions().highlightBondWidthMultiplier = 24
    d2d.drawOptions().fillHighlights = False

    draw_rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)
    atoms_to_highlight = reacting_atoms
    highligh_atom_colors = {a: color_reacting_atoms for a in reacting_atoms}
    highlight_bond_colors = {b: color_new_bonds for b in new_bonds} | {b: color_modified_bonds for b in modified_bonds}

    bonds_to_highlight = highlight_bond_colors.keys()
    d2d.DrawMolecule(draw_rdmol, highlightAtoms=atoms_to_highlight,
                     highlightAtomColors=highligh_atom_colors,
                     highlightBonds=bonds_to_highlight,
                     highlightBondColors=highlight_bond_colors)

    d2d.FinishDrawing()
    return d2d.GetDrawingText()


def draw_fragments(rdmol):
    d2d = Draw.rdMolDraw2D.MolDraw2DCairo(350, 300)
    d2d.drawOptions().useBWAtomPalette()
    d2d.drawOptions().continuousHighlight = True
    d2d.drawOptions().highlightBondWidthMultiplier = 24
    d2d.drawOptions().fillHighlights = False
    draw_rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)
    d2d.DrawMolecule(draw_rdmol)
    d2d.FinishDrawing()
    return d2d.GetDrawingText()


def draw_rxn_product_disconnection1(rxn, atms, bnds, productIdx=None, showAtomMaps=False):
    """
    https://greglandrum.github.io/rdkit-blog/tutorial/reactions/2021/11/26/highlighting-changed-bonds-in-reactions.html
    """
    if productIdx is None:
        pcnts = [x.GetNumAtoms() for x in rxn.GetProducts()]
        largestProduct = list(sorted(zip(pcnts, range(len(pcnts))), reverse=True))[0][1]

        productIdx = largestProduct
    pmol = Chem.Mol(rxn.GetProductTemplate(productIdx))
    Chem.SanitizeMol(pmol)
    if not showAtomMaps:
        for atom in pmol.GetAtoms():
            atom.SetAtomMapNum(0)
    bonds_to_highlight = []
    highlight_bond_colors = {}
    atoms_seen = set()
    for binfo in bnds:
        if binfo.product == productIdx:
            if binfo.status == 'changed':
                bonds_to_highlight.append(binfo.product_bond)
                atoms_seen.update(binfo.product_atoms)
                highlight_bond_colors[binfo.product_bond] = 0.4, 0.4, 1
            elif binfo.status == 'new':
                bonds_to_highlight.append(binfo.product_bond)
                atoms_seen.update(binfo.product_atoms)
                highlight_bond_colors[binfo.product_bond] = 1, 0.4, 0.4
    atoms_to_highlight = {ainfo.product_atom for ainfo in atms if
                          ainfo.product == productIdx and ainfo.product_atom not in atoms_seen}

    d2d = Draw.rdMolDraw2D.MolDraw2DCairo(350, 300)
    d2d.drawOptions().useBWAtomPalette()
    d2d.drawOptions().continuousHighlight = False
    d2d.drawOptions().highlightBondWidthMultiplier = 24
    d2d.drawOptions().setHighlightColour((0.9, 0.9, 0))
    d2d.drawOptions().fillHighlights = False
    atoms_to_highlight.update(atoms_seen)
    pmol = rdMolDraw2D.PrepareMolForDrawing(pmol)
    d2d.DrawMolecule(pmol, highlightAtoms=atoms_to_highlight, highlightBonds=bonds_to_highlight,
                     highlightBondColors=highlight_bond_colors)

    d2d.FinishDrawing()
    # d2d.WriteDrawingText(file_path)
    return d2d.GetDrawingText()
