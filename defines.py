import os
import pprint as pp

DEV_ID = os.environ['DEV_ID']
TOKEN = os.environ['TOKEN']
HOST_IP = os.environ['HOST_IP']
HOST_PORT = os.environ['HOST_PORT']
DONATOR1 = os.environ['DONATOR1']


##Known donators - for easteregg!##
DONATORS = [
  DONATOR1,
  #DEV_ID #for testing
]

## intervals ##
INTERVAL = 60*60
TRADE_DIS_INTERVALS = 1

##channel / server routing##
ALLOWED_SERVERS = [599153230659846165, 932389256838643755] #kaspa, test

##channels##
TRADE_OFFER_CHANS = [910316340735262720, 934846748491415573] #kaspa, test
DEDICATED_CHANS   = [934815196361404467, 934753516575158282] #kaspa, test

SER_TO_ALLOWED_CHANS = {
  599153230659846165 :{ #kaspa
    DEDICATED_CHANS[0]
  },
  932389256838643755 : [ #test 
    DEDICATED_CHANS[1]
    ]
  }

SER_TO_ANSWER_CHAN = {
  599153230659846165 : DEDICATED_CHANS[0], #kaspa
  932389256838643755 : DEDICATED_CHANS[1], #test 
}

##for kaspa backend##
TRY_DEDICATED_NODE = True

CALL_FOR_DONATION_PROB = 1/20 # more reduction 

##channels##
TRADE_OFFER_CHAN = 910316340735262720
DEVFUND_CHAN = 922204606946234398

class kaspa_constants:
  TOTAL_COIN_SUPPLY = 28_376_242_397
  INFLATIONARY_SUPPLY = 15519600*500
  DEFLATIONARY_TABLE ={
    0: {"daa_range": range(0, 15519600), "reward_per_daa": 500.0},
    1: {"daa_range": range(15519600, 18149400), "reward_per_daa": 440.0},
    2: {"daa_range": range(18149400, 20779200), "reward_per_daa": 415.30469757},
    3: {"daa_range": range(20779200, 23409000), "reward_per_daa": 391.99543598},
    4: {"daa_range": range(23409000, 26038800), "reward_per_daa": 369.99442271},
    5: {"daa_range": range(26038800, 28668600), "reward_per_daa": 349.22823143},
    6: {"daa_range": range(28668600, 31298400), "reward_per_daa": 329.62755691},
    7: {"daa_range": range(31298400, 33928200), "reward_per_daa": 311.12698372},
    8: {"daa_range": range(33928200, 36558000), "reward_per_daa": 293.66476791},
    9: {"daa_range": range(36558000, 39187800), "reward_per_daa": 277.18263097},
    10: {"daa_range": range(39187800, 41817600), "reward_per_daa": 261.6255653},
    11: {"daa_range": range(41817600, 44447400), "reward_per_daa": 246.94165062},
    12: {"daa_range": range(44447400, 47077200), "reward_per_daa": 233.08188075},
    13: {"daa_range": range(47077200, 49707000), "reward_per_daa": 220.0},
    14: {"daa_range": range(49707000, 52336800), "reward_per_daa": 207.65234878},
    15: {"daa_range": range(52336800, 54966600), "reward_per_daa": 195.99771799},
    16: {"daa_range": range(54966600, 57596400), "reward_per_daa": 184.99721135},
    17: {"daa_range": range(57596400, 60226200), "reward_per_daa": 174.61411571},
    18: {"daa_range": range(60226200, 62856000), "reward_per_daa": 164.81377845},
    19: {"daa_range": range(62856000, 65485800), "reward_per_daa": 155.56349186},
    20: {"daa_range": range(65485800, 68115600), "reward_per_daa": 146.83238395},
    21: {"daa_range": range(68115600, 70745400), "reward_per_daa": 138.59131548},
    22: {"daa_range": range(70745400, 73375200), "reward_per_daa": 130.81278265},
    23: {"daa_range": range(73375200, 76005000), "reward_per_daa": 123.47082531},
    24: {"daa_range": range(76005000, 78634800), "reward_per_daa": 116.54094037},
    25: {"daa_range": range(78634800, 81264600), "reward_per_daa": 110.0},
    26: {"daa_range": range(81264600, 83894400), "reward_per_daa": 103.82617439},
    27: {"daa_range": range(83894400, 86524200), "reward_per_daa": 97.99885899},
    28: {"daa_range": range(86524200, 89154000), "reward_per_daa": 92.49860567},
    29: {"daa_range": range(89154000, 91783800), "reward_per_daa": 87.30705785},
    30: {"daa_range": range(91783800, 94413600), "reward_per_daa": 82.40688922},
    31: {"daa_range": range(94413600, 97043400), "reward_per_daa": 77.78174593},
    32: {"daa_range": range(97043400, 99673200), "reward_per_daa": 73.41619197},
    33: {"daa_range": range(99673200, 102303000), "reward_per_daa": 69.29565774},
    34: {"daa_range": range(102303000, 104932800), "reward_per_daa": 65.40639132},
    35: {"daa_range": range(104932800, 107562600), "reward_per_daa": 61.73541265},
    36: {"daa_range": range(107562600, 110192400), "reward_per_daa": 58.27047018},
    37: {"daa_range": range(110192400, 112822200), "reward_per_daa": 55.0},
    38: {"daa_range": range(112822200, 115452000), "reward_per_daa": 51.91308719},
    39: {"daa_range": range(115452000, 118081800), "reward_per_daa": 48.99942949},
    40: {"daa_range": range(118081800, 120711600), "reward_per_daa": 46.24930283},
    41: {"daa_range": range(120711600, 123341400), "reward_per_daa": 43.65352892},
    42: {"daa_range": range(123341400, 125971200), "reward_per_daa": 41.20344461},
    43: {"daa_range": range(125971200, 128601000), "reward_per_daa": 38.89087296},
    44: {"daa_range": range(128601000, 131230800), "reward_per_daa": 36.70809598},
    45: {"daa_range": range(131230800, 133860600), "reward_per_daa": 34.64782887},
    46: {"daa_range": range(133860600, 136490400), "reward_per_daa": 32.70319566},
    47: {"daa_range": range(136490400, 139120200), "reward_per_daa": 30.86770632},
    48: {"daa_range": range(139120200, 141750000), "reward_per_daa": 29.13523509},
    49: {"daa_range": range(141750000, 144379800), "reward_per_daa": 27.5},
    50: {"daa_range": range(144379800, 147009600), "reward_per_daa": 25.95654359},
    51: {"daa_range": range(147009600, 149639400), "reward_per_daa": 24.49971474},
    52: {"daa_range": range(149639400, 152269200), "reward_per_daa": 23.12465141},
    53: {"daa_range": range(152269200, 154899000), "reward_per_daa": 21.82676446},
    54: {"daa_range": range(154899000, 157528800), "reward_per_daa": 20.6017223},
    55: {"daa_range": range(157528800, 160158600), "reward_per_daa": 19.44543648},
    56: {"daa_range": range(160158600, 162788400), "reward_per_daa": 18.35404799},
    57: {"daa_range": range(162788400, 165418200), "reward_per_daa": 17.32391443},
    58: {"daa_range": range(165418200, 168048000), "reward_per_daa": 16.35159783},
    59: {"daa_range": range(168048000, 170677800), "reward_per_daa": 15.43385316},
    60: {"daa_range": range(170677800, 173307600), "reward_per_daa": 14.56761754},
    61: {"daa_range": range(173307600, 175937400), "reward_per_daa": 13.75},
    62: {"daa_range": range(175937400, 178567200), "reward_per_daa": 12.97827179},
    63: {"daa_range": range(178567200, 181197000), "reward_per_daa": 12.24985737},
    64: {"daa_range": range(181197000, 183826800), "reward_per_daa": 11.5623257},
    65: {"daa_range": range(183826800, 186456600), "reward_per_daa": 10.91338223},
    66: {"daa_range": range(186456600, 189086400), "reward_per_daa": 10.30086115},
    67: {"daa_range": range(189086400, 191716200), "reward_per_daa": 9.72271824},
    68: {"daa_range": range(191716200, 194346000), "reward_per_daa": 9.17702399},
    69: {"daa_range": range(194346000, 196975800), "reward_per_daa": 8.66195721},
    70: {"daa_range": range(196975800, 199605600), "reward_per_daa": 8.17579891},
    71: {"daa_range": range(199605600, 202235400), "reward_per_daa": 7.71692658},
    72: {"daa_range": range(202235400, 204865200), "reward_per_daa": 7.28380877},
    73: {"daa_range": range(204865200, 207495000), "reward_per_daa": 6.875},
    74: {"daa_range": range(207495000, 210124800), "reward_per_daa": 6.48913589},
    75: {"daa_range": range(210124800, 212754600), "reward_per_daa": 6.12492868},
    76: {"daa_range": range(212754600, 215384400), "reward_per_daa": 5.78116285},
    77: {"daa_range": range(215384400, 218014200), "reward_per_daa": 5.45669111},
    78: {"daa_range": range(218014200, 220644000), "reward_per_daa": 5.15043057},
    79: {"daa_range": range(220644000, 223273800), "reward_per_daa": 4.86135912},
    80: {"daa_range": range(223273800, 225903600), "reward_per_daa": 4.58851199},
    81: {"daa_range": range(225903600, 228533400), "reward_per_daa": 4.3309786},
    82: {"daa_range": range(228533400, 231163200), "reward_per_daa": 4.08789945},
    83: {"daa_range": range(231163200, 233793000), "reward_per_daa": 3.85846329},
    84: {"daa_range": range(233793000, 236422800), "reward_per_daa": 3.64190438},
    85: {"daa_range": range(236422800, 239052600), "reward_per_daa": 3.4375},
    86: {"daa_range": range(239052600, 241682400), "reward_per_daa": 3.24456794},
    87: {"daa_range": range(241682400, 244312200), "reward_per_daa": 3.06246434},
    88: {"daa_range": range(244312200, 246942000), "reward_per_daa": 2.89058142},
    89: {"daa_range": range(246942000, 249571800), "reward_per_daa": 2.72834555},
    90: {"daa_range": range(249571800, 252201600), "reward_per_daa": 2.57521528},
    91: {"daa_range": range(252201600, 254831400), "reward_per_daa": 2.43067956},
    92: {"daa_range": range(254831400, 257461200), "reward_per_daa": 2.29425599},
    93: {"daa_range": range(257461200, 260091000), "reward_per_daa": 2.1654893},
    94: {"daa_range": range(260091000, 262720800), "reward_per_daa": 2.04394972},
    95: {"daa_range": range(262720800, 265350600), "reward_per_daa": 1.92923164},
    96: {"daa_range": range(265350600, 267980400), "reward_per_daa": 1.82095219},
    97: {"daa_range": range(267980400, 270610200), "reward_per_daa": 1.71875},
    98: {"daa_range": range(270610200, 273240000), "reward_per_daa": 1.62228397},
    99: {"daa_range": range(273240000, 275869800), "reward_per_daa": 1.53123217},
    100: {"daa_range": range(275869800, 278499600), "reward_per_daa": 1.44529071},
    101: {"daa_range": range(278499600, 281129400), "reward_per_daa": 1.36417277},
    102: {"daa_range": range(281129400, 283759200), "reward_per_daa": 1.28760764},
    103: {"daa_range": range(283759200, 286389000), "reward_per_daa": 1.21533978},
    104: {"daa_range": range(286389000, 289018800), "reward_per_daa": 1.14712799},
    105: {"daa_range": range(289018800, 291648600), "reward_per_daa": 1.08274465},
    106: {"daa_range": range(291648600, 294278400), "reward_per_daa": 1.02197486},
    107: {"daa_range": range(294278400, 296908200), "reward_per_daa": 0.96461582},
    108: {"daa_range": range(296908200, 299538000), "reward_per_daa": 0.91047609},
    109: {"daa_range": range(299538000, 302167800), "reward_per_daa": 0.859375},
    110: {"daa_range": range(302167800, 304797600), "reward_per_daa": 0.81114198},
    111: {"daa_range": range(304797600, 307427400), "reward_per_daa": 0.76561608},
    112: {"daa_range": range(307427400, 310057200), "reward_per_daa": 0.72264535},
    113: {"daa_range": range(310057200, 312687000), "reward_per_daa": 0.68208638},
    114: {"daa_range": range(312687000, 315316800), "reward_per_daa": 0.64380382},
    115: {"daa_range": range(315316800, 317946600), "reward_per_daa": 0.60766989},
    116: {"daa_range": range(317946600, 320576400), "reward_per_daa": 0.57356399},
    117: {"daa_range": range(320576400, 323206200), "reward_per_daa": 0.54137232},
    118: {"daa_range": range(323206200, 325836000), "reward_per_daa": 0.51098743},
    119: {"daa_range": range(325836000, 328465800), "reward_per_daa": 0.48230791},
    120: {"daa_range": range(328465800, 331095600), "reward_per_daa": 0.45523804},
    121: {"daa_range": range(331095600, 333725400), "reward_per_daa": 0.4296875},
    122: {"daa_range": range(333725400, 336355200), "reward_per_daa": 0.40557099},
    123: {"daa_range": range(336355200, 338985000), "reward_per_daa": 0.38280804},
    124: {"daa_range": range(338985000, 341614800), "reward_per_daa": 0.36132267},
    125: {"daa_range": range(341614800, 344244600), "reward_per_daa": 0.34104319},
    126: {"daa_range": range(344244600, 346874400), "reward_per_daa": 0.32190191},
    127: {"daa_range": range(346874400, 349504200), "reward_per_daa": 0.30383494},
    128: {"daa_range": range(349504200, 352134000), "reward_per_daa": 0.28678199},
    129: {"daa_range": range(352134000, 354763800), "reward_per_daa": 0.27068616},
    130: {"daa_range": range(354763800, 357393600), "reward_per_daa": 0.25549371},
    131: {"daa_range": range(357393600, 360023400), "reward_per_daa": 0.24115395},
    132: {"daa_range": range(360023400, 362653200), "reward_per_daa": 0.22761902},
    133: {"daa_range": range(362653200, 365283000), "reward_per_daa": 0.21484375},
    134: {"daa_range": range(365283000, 367912800), "reward_per_daa": 0.20278549},
    135: {"daa_range": range(367912800, 370542600), "reward_per_daa": 0.19140402},
    136: {"daa_range": range(370542600, 373172400), "reward_per_daa": 0.18066133},
    137: {"daa_range": range(373172400, 375802200), "reward_per_daa": 0.17052159},
    138: {"daa_range": range(375802200, 378432000), "reward_per_daa": 0.16095095},
    139: {"daa_range": range(378432000, 381061800), "reward_per_daa": 0.15191747},
    140: {"daa_range": range(381061800, 383691600), "reward_per_daa": 0.14339099},
    141: {"daa_range": range(383691600, 386321400), "reward_per_daa": 0.13534308},
    142: {"daa_range": range(386321400, 388951200), "reward_per_daa": 0.12774685},
    143: {"daa_range": range(388951200, 391581000), "reward_per_daa": 0.12057697},
    144: {"daa_range": range(391581000, 394210800), "reward_per_daa": 0.11380951},
    145: {"daa_range": range(394210800, 396840600), "reward_per_daa": 0.10742187},
    146: {"daa_range": range(396840600, 399470400), "reward_per_daa": 0.10139274},
    147: {"daa_range": range(399470400, 402100200), "reward_per_daa": 0.09570201},
    148: {"daa_range": range(402100200, 404730000), "reward_per_daa": 0.09033066},
    149: {"daa_range": range(404730000, 407359800), "reward_per_daa": 0.08526079},
    150: {"daa_range": range(407359800, 409989600), "reward_per_daa": 0.08047547},
    151: {"daa_range": range(409989600, 412619400), "reward_per_daa": 0.07595873},
    152: {"daa_range": range(412619400, 415249200), "reward_per_daa": 0.07169549},
    153: {"daa_range": range(415249200, 417879000), "reward_per_daa": 0.06767154},
    154: {"daa_range": range(417879000, 420508800), "reward_per_daa": 0.06387342},
    155: {"daa_range": range(420508800, 423138600), "reward_per_daa": 0.06028848},
    156: {"daa_range": range(423138600, 425768400), "reward_per_daa": 0.05690475},
    157: {"daa_range": range(425768400, 428398200), "reward_per_daa": 0.05371093},
    158: {"daa_range": range(428398200, 431028000), "reward_per_daa": 0.05069637},
    159: {"daa_range": range(431028000, 433657800), "reward_per_daa": 0.047851},
    160: {"daa_range": range(433657800, 436287600), "reward_per_daa": 0.04516533},
    161: {"daa_range": range(436287600, 438917400), "reward_per_daa": 0.04263039},
    162: {"daa_range": range(438917400, 441547200), "reward_per_daa": 0.04023773},
    163: {"daa_range": range(441547200, 444177000), "reward_per_daa": 0.03797936},
    164: {"daa_range": range(444177000, 446806800), "reward_per_daa": 0.03584774},
    165: {"daa_range": range(446806800, 449436600), "reward_per_daa": 0.03383577},
    166: {"daa_range": range(449436600, 452066400), "reward_per_daa": 0.03193671},
    167: {"daa_range": range(452066400, 454696200), "reward_per_daa": 0.03014424},
    168: {"daa_range": range(454696200, 457326000), "reward_per_daa": 0.02845237},
    169: {"daa_range": range(457326000, 459955800), "reward_per_daa": 0.02685546},
    170: {"daa_range": range(459955800, 462585600), "reward_per_daa": 0.02534818},
    171: {"daa_range": range(462585600, 465215400), "reward_per_daa": 0.0239255},
    172: {"daa_range": range(465215400, 467845200), "reward_per_daa": 0.02258266},
    173: {"daa_range": range(467845200, 470475000), "reward_per_daa": 0.02131519},
    174: {"daa_range": range(470475000, 473104800), "reward_per_daa": 0.02011886},
    175: {"daa_range": range(473104800, 475734600), "reward_per_daa": 0.01898968},
    176: {"daa_range": range(475734600, 478364400), "reward_per_daa": 0.01792387},
    177: {"daa_range": range(478364400, 480994200), "reward_per_daa": 0.01691788},
    178: {"daa_range": range(480994200, 483624000), "reward_per_daa": 0.01596835},
    179: {"daa_range": range(483624000, 486253800), "reward_per_daa": 0.01507212},
    180: {"daa_range": range(486253800, 488883600), "reward_per_daa": 0.01422618},
    181: {"daa_range": range(488883600, 491513400), "reward_per_daa": 0.01342773},
    182: {"daa_range": range(491513400, 494143200), "reward_per_daa": 0.01267409},
    183: {"daa_range": range(494143200, 496773000), "reward_per_daa": 0.01196275},
    184: {"daa_range": range(496773000, 499402800), "reward_per_daa": 0.01129133},
    185: {"daa_range": range(499402800, 502032600), "reward_per_daa": 0.01065759},
    186: {"daa_range": range(502032600, 504662400), "reward_per_daa": 0.01005943},
    187: {"daa_range": range(504662400, 507292200), "reward_per_daa": 0.00949484},
    188: {"daa_range": range(507292200, 509922000), "reward_per_daa": 0.00896193},
    189: {"daa_range": range(509922000, 512551800), "reward_per_daa": 0.00845894},
    190: {"daa_range": range(512551800, 515181600), "reward_per_daa": 0.00798417},
    191: {"daa_range": range(515181600, 517811400), "reward_per_daa": 0.00753606},
    192: {"daa_range": range(517811400, 520441200), "reward_per_daa": 0.00711309},
    193: {"daa_range": range(520441200, 523071000), "reward_per_daa": 0.00671386},
    194: {"daa_range": range(523071000, 525700800), "reward_per_daa": 0.00633704},
    195: {"daa_range": range(525700800, 528330600), "reward_per_daa": 0.00598137},
    196: {"daa_range": range(528330600, 530960400), "reward_per_daa": 0.00564566},
    197: {"daa_range": range(530960400, 533590200), "reward_per_daa": 0.00532879},
    198: {"daa_range": range(533590200, 536220000), "reward_per_daa": 0.00502971},
    199: {"daa_range": range(536220000, 538849800), "reward_per_daa": 0.00474742},
    200: {"daa_range": range(538849800, 541479600), "reward_per_daa": 0.00448096},
    201: {"daa_range": range(541479600, 544109400), "reward_per_daa": 0.00422947},
    202: {"daa_range": range(544109400, 546739200), "reward_per_daa": 0.00399208},
    203: {"daa_range": range(546739200, 549369000), "reward_per_daa": 0.00376803},
    204: {"daa_range": range(549369000, 551998800), "reward_per_daa": 0.00355654},
    205: {"daa_range": range(551998800, 554628600), "reward_per_daa": 0.00335693},
    206: {"daa_range": range(554628600, 557258400), "reward_per_daa": 0.00316852},
    207: {"daa_range": range(557258400, 559888200), "reward_per_daa": 0.00299068},
    208: {"daa_range": range(559888200, 562518000), "reward_per_daa": 0.00282283},
    209: {"daa_range": range(562518000, 565147800), "reward_per_daa": 0.00266439},
    210: {"daa_range": range(565147800, 567777600), "reward_per_daa": 0.00251485},
    211: {"daa_range": range(567777600, 570407400), "reward_per_daa": 0.00237371},
    212: {"daa_range": range(570407400, 573037200), "reward_per_daa": 0.00224048},
    213: {"daa_range": range(573037200, 575667000), "reward_per_daa": 0.00211473},
    214: {"daa_range": range(575667000, 578296800), "reward_per_daa": 0.00199604},
    215: {"daa_range": range(578296800, 580926600), "reward_per_daa": 0.00188401},
    216: {"daa_range": range(580926600, 583556400), "reward_per_daa": 0.00177827},
    217: {"daa_range": range(583556400, 586186200), "reward_per_daa": 0.00167846},
    218: {"daa_range": range(586186200, 588816000), "reward_per_daa": 0.00158426},
    219: {"daa_range": range(588816000, 591445800), "reward_per_daa": 0.00149534},
    220: {"daa_range": range(591445800, 594075600), "reward_per_daa": 0.00141141},
    221: {"daa_range": range(594075600, 596705400), "reward_per_daa": 0.00133219},
    222: {"daa_range": range(596705400, 599335200), "reward_per_daa": 0.00125742},
    223: {"daa_range": range(599335200, 601965000), "reward_per_daa": 0.00118685},
    224: {"daa_range": range(601965000, 604594800), "reward_per_daa": 0.00112024},
    225: {"daa_range": range(604594800, 607224600), "reward_per_daa": 0.00105736},
    226: {"daa_range": range(607224600, 609854400), "reward_per_daa": 0.00099802},
    227: {"daa_range": range(609854400, 612484200), "reward_per_daa": 0.000942},
    228: {"daa_range": range(612484200, 615114000), "reward_per_daa": 0.00088913},
    229: {"daa_range": range(615114000, 617743800), "reward_per_daa": 0.00083923},
    230: {"daa_range": range(617743800, 620373600), "reward_per_daa": 0.00079213},
    231: {"daa_range": range(620373600, 623003400), "reward_per_daa": 0.00074767},
    232: {"daa_range": range(623003400, 625633200), "reward_per_daa": 0.0007057},
    233: {"daa_range": range(625633200, 628263000), "reward_per_daa": 0.00066609},
    234: {"daa_range": range(628263000, 630892800), "reward_per_daa": 0.00062871},
    235: {"daa_range": range(630892800, 633522600), "reward_per_daa": 0.00059342},
    236: {"daa_range": range(633522600, 636152400), "reward_per_daa": 0.00056012},
    237: {"daa_range": range(636152400, 638782200), "reward_per_daa": 0.00052868},
    238: {"daa_range": range(638782200, 641412000), "reward_per_daa": 0.00049901},
    239: {"daa_range": range(641412000, 644041800), "reward_per_daa": 0.000471},
    240: {"daa_range": range(644041800, 646671600), "reward_per_daa": 0.00044456},
    241: {"daa_range": range(646671600, 649301400), "reward_per_daa": 0.00041961},
    242: {"daa_range": range(649301400, 651931200), "reward_per_daa": 0.00039606},
    243: {"daa_range": range(651931200, 654561000), "reward_per_daa": 0.00037383},
    244: {"daa_range": range(654561000, 657190800), "reward_per_daa": 0.00035285},
    245: {"daa_range": range(657190800, 659820600), "reward_per_daa": 0.00033304},
    246: {"daa_range": range(659820600, 662450400), "reward_per_daa": 0.00031435},
    247: {"daa_range": range(662450400, 665080200), "reward_per_daa": 0.00029671},
    248: {"daa_range": range(665080200, 667710000), "reward_per_daa": 0.00028006},
    249: {"daa_range": range(667710000, 670339800), "reward_per_daa": 0.00026434},
    250: {"daa_range": range(670339800, 672969600), "reward_per_daa": 0.0002495},
    251: {"daa_range": range(672969600, 675599400), "reward_per_daa": 0.0002355},
    252: {"daa_range": range(675599400, 678229200), "reward_per_daa": 0.00022228},
    253: {"daa_range": range(678229200, 680859000), "reward_per_daa": 0.0002098},
    254: {"daa_range": range(680859000, 683488800), "reward_per_daa": 0.00019803},
    255: {"daa_range": range(683488800, 686118600), "reward_per_daa": 0.00018691},
    256: {"daa_range": range(686118600, 688748400), "reward_per_daa": 0.00017642},
    257: {"daa_range": range(688748400, 691378200), "reward_per_daa": 0.00016652},
    258: {"daa_range": range(691378200, 694008000), "reward_per_daa": 0.00015717},
    259: {"daa_range": range(694008000, 696637800), "reward_per_daa": 0.00014835},
    260: {"daa_range": range(696637800, 699267600), "reward_per_daa": 0.00014003},
    261: {"daa_range": range(699267600, 701897400), "reward_per_daa": 0.00013217},
    262: {"daa_range": range(701897400, 704527200), "reward_per_daa": 0.00012475},
    263: {"daa_range": range(704527200, 707157000), "reward_per_daa": 0.00011775},
    264: {"daa_range": range(707157000, 709786800), "reward_per_daa": 0.00011114},
    265: {"daa_range": range(709786800, 712416600), "reward_per_daa": 0.0001049},
    266: {"daa_range": range(712416600, 715046400), "reward_per_daa": 9.901e-05},
    267: {"daa_range": range(715046400, 717676200), "reward_per_daa": 9.345e-05},
    268: {"daa_range": range(717676200, 720306000), "reward_per_daa": 8.821e-05},
    269: {"daa_range": range(720306000, 722935800), "reward_per_daa": 8.326e-05},
    270: {"daa_range": range(722935800, 725565600), "reward_per_daa": 7.858e-05},
    271: {"daa_range": range(725565600, 728195400), "reward_per_daa": 7.417e-05},
    272: {"daa_range": range(728195400, 730825200), "reward_per_daa": 7.001e-05},
    273: {"daa_range": range(730825200, 733455000), "reward_per_daa": 6.608e-05},
    274: {"daa_range": range(733455000, 736084800), "reward_per_daa": 6.237e-05},
    275: {"daa_range": range(736084800, 738714600), "reward_per_daa": 5.887e-05},
    276: {"daa_range": range(738714600, 741344400), "reward_per_daa": 5.557e-05},
    277: {"daa_range": range(741344400, 743974200), "reward_per_daa": 5.245e-05},
    278: {"daa_range": range(743974200, 746604000), "reward_per_daa": 4.95e-05},
    279: {"daa_range": range(746604000, 749233800), "reward_per_daa": 4.672e-05},
    280: {"daa_range": range(749233800, 751863600), "reward_per_daa": 4.41e-05},
    281: {"daa_range": range(751863600, 754493400), "reward_per_daa": 4.163e-05},
    282: {"daa_range": range(754493400, 757123200), "reward_per_daa": 3.929e-05},
    283: {"daa_range": range(757123200, 759753000), "reward_per_daa": 3.708e-05},
    284: {"daa_range": range(759753000, 762382800), "reward_per_daa": 3.5e-05},
    285: {"daa_range": range(762382800, 765012600), "reward_per_daa": 3.304e-05},
    286: {"daa_range": range(765012600, 767642400), "reward_per_daa": 3.118e-05},
    287: {"daa_range": range(767642400, 770272200), "reward_per_daa": 2.943e-05},
    288: {"daa_range": range(770272200, 772902000), "reward_per_daa": 2.778e-05},
    289: {"daa_range": range(772902000, 775531800), "reward_per_daa": 2.622e-05},
    290: {"daa_range": range(775531800, 778161600), "reward_per_daa": 2.475e-05},
    291: {"daa_range": range(778161600, 780791400), "reward_per_daa": 2.336e-05},
    292: {"daa_range": range(780791400, 783421200), "reward_per_daa": 2.205e-05},
    293: {"daa_range": range(783421200, 786051000), "reward_per_daa": 2.081e-05},
    294: {"daa_range": range(786051000, 788680800), "reward_per_daa": 1.964e-05},
    295: {"daa_range": range(788680800, 791310600), "reward_per_daa": 1.854e-05},
    296: {"daa_range": range(791310600, 793940400), "reward_per_daa": 1.75e-05},
    297: {"daa_range": range(793940400, 796570200), "reward_per_daa": 1.652e-05},
    298: {"daa_range": range(796570200, 799200000), "reward_per_daa": 1.559e-05},
    299: {"daa_range": range(799200000, 801829800), "reward_per_daa": 1.471e-05},
    300: {"daa_range": range(801829800, 804459600), "reward_per_daa": 1.389e-05},
    301: {"daa_range": range(804459600, 807089400), "reward_per_daa": 1.311e-05},
    302: {"daa_range": range(807089400, 809719200), "reward_per_daa": 1.237e-05},
    303: {"daa_range": range(809719200, 812349000), "reward_per_daa": 1.168e-05},
    304: {"daa_range": range(812349000, 814978800), "reward_per_daa": 1.102e-05},
    305: {"daa_range": range(814978800, 817608600), "reward_per_daa": 1.04e-05},
    306: {"daa_range": range(817608600, 820238400), "reward_per_daa": 9.82e-06},
    307: {"daa_range": range(820238400, 822868200), "reward_per_daa": 9.27e-06},
    308: {"daa_range": range(822868200, 825498000), "reward_per_daa": 8.75e-06},
    309: {"daa_range": range(825498000, 828127800), "reward_per_daa": 8.26e-06},
    310: {"daa_range": range(828127800, 830757600), "reward_per_daa": 7.79e-06},
    311: {"daa_range": range(830757600, 833387400), "reward_per_daa": 7.35e-06},
    312: {"daa_range": range(833387400, 836017200), "reward_per_daa": 6.94e-06},
    313: {"daa_range": range(836017200, 838647000), "reward_per_daa": 6.55e-06},
    314: {"daa_range": range(838647000, 841276800), "reward_per_daa": 6.18e-06},
    315: {"daa_range": range(841276800, 843906600), "reward_per_daa": 5.84e-06},
    316: {"daa_range": range(843906600, 846536400), "reward_per_daa": 5.51e-06},
    317: {"daa_range": range(846536400, 849166200), "reward_per_daa": 5.2e-06},
    318: {"daa_range": range(849166200, 851796000), "reward_per_daa": 4.91e-06},
    319: {"daa_range": range(851796000, 854425800), "reward_per_daa": 4.63e-06},
    320: {"daa_range": range(854425800, 857055600), "reward_per_daa": 4.37e-06},
    321: {"daa_range": range(857055600, 859685400), "reward_per_daa": 4.13e-06},
    322: {"daa_range": range(859685400, 862315200), "reward_per_daa": 3.89e-06},
    323: {"daa_range": range(862315200, 864945000), "reward_per_daa": 3.67e-06},
    324: {"daa_range": range(864945000, 867574800), "reward_per_daa": 3.47e-06},
    325: {"daa_range": range(867574800, 870204600), "reward_per_daa": 3.27e-06},
    326: {"daa_range": range(870204600, 872834400), "reward_per_daa": 3.09e-06},
    327: {"daa_range": range(872834400, 875464200), "reward_per_daa": 2.92e-06},
    328: {"daa_range": range(875464200, 878094000), "reward_per_daa": 2.75e-06},
    329: {"daa_range": range(878094000, 880723800), "reward_per_daa": 2.6e-06},
    330: {"daa_range": range(880723800, 883353600), "reward_per_daa": 2.45e-06},
    331: {"daa_range": range(883353600, 885983400), "reward_per_daa": 2.31e-06},
    332: {"daa_range": range(885983400, 888613200), "reward_per_daa": 2.18e-06},
    333: {"daa_range": range(888613200, 891243000), "reward_per_daa": 2.06e-06},
    334: {"daa_range": range(891243000, 893872800), "reward_per_daa": 1.94e-06},
    335: {"daa_range": range(893872800, 896502600), "reward_per_daa": 1.83e-06},
    336: {"daa_range": range(896502600, 899132400), "reward_per_daa": 1.73e-06},
    337: {"daa_range": range(899132400, 901762200), "reward_per_daa": 1.63e-06},
    338: {"daa_range": range(901762200, 904392000), "reward_per_daa": 1.54e-06},
    339: {"daa_range": range(904392000, 907021800), "reward_per_daa": 1.46e-06},
    340: {"daa_range": range(907021800, 909651600), "reward_per_daa": 1.37e-06},
    341: {"daa_range": range(909651600, 912281400), "reward_per_daa": 1.3e-06},
    342: {"daa_range": range(912281400, 914911200), "reward_per_daa": 1.22e-06},
    343: {"daa_range": range(914911200, 917541000), "reward_per_daa": 1.15e-06},
    344: {"daa_range": range(917541000, 920170800), "reward_per_daa": 1.09e-06},
    345: {"daa_range": range(920170800, 922800600), "reward_per_daa": 1.03e-06},
    346: {"daa_range": range(922800600, 925430400), "reward_per_daa": 9.7e-07},
    347: {"daa_range": range(925430400, 928060200), "reward_per_daa": 9.1e-07},
    348: {"daa_range": range(928060200, 930690000), "reward_per_daa": 8.6e-07},
    349: {"daa_range": range(930690000, 933319800), "reward_per_daa": 8.1e-07},
    350: {"daa_range": range(933319800, 935949600), "reward_per_daa": 7.7e-07},
    351: {"daa_range": range(935949600, 938579400), "reward_per_daa": 7.3e-07},
    352: {"daa_range": range(938579400, 941209200), "reward_per_daa": 6.8e-07},
    353: {"daa_range": range(941209200, 943839000), "reward_per_daa": 6.5e-07},
    354: {"daa_range": range(943839000, 946468800), "reward_per_daa": 6.1e-07},
    355: {"daa_range": range(946468800, 949098600), "reward_per_daa": 5.7e-07},
    356: {"daa_range": range(949098600, 951728400), "reward_per_daa": 5.4e-07},
    357: {"daa_range": range(951728400, 954358200), "reward_per_daa": 5.1e-07},
    358: {"daa_range": range(954358200, 956988000), "reward_per_daa": 4.8e-07},
    359: {"daa_range": range(956988000, 959617800), "reward_per_daa": 4.5e-07},
    360: {"daa_range": range(959617800, 962247600), "reward_per_daa": 4.3e-07},
    361: {"daa_range": range(962247600, 964877400), "reward_per_daa": 4e-07},
    362: {"daa_range": range(964877400, 967507200), "reward_per_daa": 3.8e-07},
    363: {"daa_range": range(967507200, 970137000), "reward_per_daa": 3.6e-07},
    364: {"daa_range": range(970137000, 972766800), "reward_per_daa": 3.4e-07},
    365: {"daa_range": range(972766800, 975396600), "reward_per_daa": 3.2e-07},
    366: {"daa_range": range(975396600, 978026400), "reward_per_daa": 3e-07},
    367: {"daa_range": range(978026400, 980656200), "reward_per_daa": 2.8e-07},
    368: {"daa_range": range(980656200, 983286000), "reward_per_daa": 2.7e-07},
    369: {"daa_range": range(983286000, 985915800), "reward_per_daa": 2.5e-07},
    370: {"daa_range": range(985915800, 988545600), "reward_per_daa": 2.4e-07},
    371: {"daa_range": range(988545600, 991175400), "reward_per_daa": 2.2e-07},
    372: {"daa_range": range(991175400, 993805200), "reward_per_daa": 2.1e-07},
    373: {"daa_range": range(993805200, 996435000), "reward_per_daa": 2e-07},
    374: {"daa_range": range(996435000, 999064800), "reward_per_daa": 1.9e-07},
    375: {"daa_range": range(999064800, 1001694600), "reward_per_daa": 1.8e-07},
    376: {"daa_range": range(1001694600, 1004324400), "reward_per_daa": 1.7e-07},
    377: {"daa_range": range(1004324400, 1006954200), "reward_per_daa": 1.6e-07},
    378: {"daa_range": range(1006954200, 1009584000), "reward_per_daa": 1.5e-07},
    379: {"daa_range": range(1009584000, 1012213800), "reward_per_daa": 1.4e-07},
    380: {"daa_range": range(1012213800, 1014843600), "reward_per_daa": 1.3e-07},
    381: {"daa_range": range(1014843600, 1017473400), "reward_per_daa": 1.2e-07},
    382: {"daa_range": range(1017473400, 1020103200), "reward_per_daa": 1.2e-07},
    383: {"daa_range": range(1020103200, 1022733000), "reward_per_daa": 1.1e-07},
    384: {"daa_range": range(1022733000, 1025362800), "reward_per_daa": 1e-07},
    385: {"daa_range": range(1025362800, 1027992600), "reward_per_daa": 1e-07},
    386: {"daa_range": range(1027992600, 1030622400), "reward_per_daa": 9e-08},
    387: {"daa_range": range(1030622400, 1033252200), "reward_per_daa": 9e-08},
    388: {"daa_range": range(1033252200, 1035882000), "reward_per_daa": 8e-08},
    389: {"daa_range": range(1035882000, 1038511800), "reward_per_daa": 8e-08},
    390: {"daa_range": range(1038511800, 1041141600), "reward_per_daa": 7e-08},
    391: {"daa_range": range(1041141600, 1043771400), "reward_per_daa": 7e-08},
    392: {"daa_range": range(1043771400, 1046401200), "reward_per_daa": 6e-08},
    393: {"daa_range": range(1046401200, 1049031000), "reward_per_daa": 6e-08},
    394: {"daa_range": range(1049031000, 1051660800), "reward_per_daa": 6e-08},
    395: {"daa_range": range(1051660800, 1054290600), "reward_per_daa": 5e-08},
    396: {"daa_range": range(1054290600, 1056920400), "reward_per_daa": 5e-08},
    397: {"daa_range": range(1056920400, 1059550200), "reward_per_daa": 5e-08},
    398: {"daa_range": range(1059550200, 1062180000), "reward_per_daa": 4e-08},
    399: {"daa_range": range(1062180000, 1064809800), "reward_per_daa": 4e-08},
    400: {"daa_range": range(1064809800, 1067439600), "reward_per_daa": 4e-08},
    401: {"daa_range": range(1067439600, 1070069400), "reward_per_daa": 4e-08},
    402: {"daa_range": range(1070069400, 1072699200), "reward_per_daa": 3e-08},
    403: {"daa_range": range(1072699200, 1075329000), "reward_per_daa": 3e-08},
    404: {"daa_range": range(1075329000, 1077958800), "reward_per_daa": 3e-08},
    405: {"daa_range": range(1077958800, 1080588600), "reward_per_daa": 3e-08},
    406: {"daa_range": range(1080588600, 1083218400), "reward_per_daa": 3e-08},
    407: {"daa_range": range(1083218400, 1085848200), "reward_per_daa": 2e-08},
    408: {"daa_range": range(1085848200, 1088478000), "reward_per_daa": 2e-08},
    409: {"daa_range": range(1088478000, 1091107800), "reward_per_daa": 2e-08},
    410: {"daa_range": range(1091107800, 1093737600), "reward_per_daa": 2e-08},
    411: {"daa_range": range(1093737600, 1096367400), "reward_per_daa": 2e-08},
    412: {"daa_range": range(1096367400, 1098997200), "reward_per_daa": 2e-08},
    413: {"daa_range": range(1098997200, 1101627000), "reward_per_daa": 2e-08},
    414: {"daa_range": range(1101627000, 1104256800), "reward_per_daa": 1e-08},
    415: {"daa_range": range(1104256800, 1106886600), "reward_per_daa": 1e-08},
    416: {"daa_range": range(1106886600, 1109516400), "reward_per_daa": 1e-08},
    417: {"daa_range": range(1109516400, 1112146200), "reward_per_daa": 1e-08},
    418: {"daa_range": range(1112146200, 1114776000), "reward_per_daa": 1e-08},
    419: {"daa_range": range(1114776000, 1117405800), "reward_per_daa": 1e-08},
    420: {"daa_range": range(1117405800, 1120035600), "reward_per_daa": 1e-08},
    421: {"daa_range": range(1120035600, 1122665400), "reward_per_daa": 1e-08},
    422: {"daa_range": range(1122665400, 1125295200), "reward_per_daa": 1e-08},
    423: {"daa_range": range(1125295200, 1127925000), "reward_per_daa": 1e-08},
    424: {"daa_range": range(1127925000, 1130554800), "reward_per_daa": 1e-08},
    425: {"daa_range": range(1130554800, 1133184600), "reward_per_daa": 1e-08},
    426: {"daa_range": range(1133184600, 9223372036854775807), "reward_per_daa": 0.0},
}


class devfund_addresses:
    MINING_ADDR = 'kaspa:pzhh76qc82wzduvsrd9xh4zde9qhp0xc8rl7qu2mvl2e42uvdqt75zrcgpm00'
    DONATION_ADDR = 'kaspa:precqv0krj3r6uyyfa36ga7s0u9jct0v4wg8ctsfde2gkrsgwgw8jgxfzfc98'

class kasper_addresses:
    DONATION_ADDR = 'kaspa:qp33anhdnnsfzg474jd3s5csuaf0k9kn6cvy3pfcx9rnezak5qkhgskuztcum'

class answers:
    DISCLAIMER = '''Disclaimer:
  
  This is a kind reminder that #trade channel is not moderated by the server mods, core devs, treasurers or any other constituents of the Kaspa community. This channel was created to accommodate traders which bogged down the community channel, having created it does not impose any responsibility for the actions of any buyer, seller, escrow service etc. on any particular community member. Please be mindful of that and careful with your money.'''

    FAILED = lambda recv_msg : f'''
  Could not process: {recv_msg}'''

    SUCCESS = f'''SUCCESS''' # for test command

    DAG_STATS =lambda stats : f'''{pp.pformat(stats)}'''

    COIN_STATS = lambda circulating_coins : f'''
    Circulating supply  : {circulating_coins:,}
    Total supply        : {kaspa_constants.TOTAL_COIN_SUPPLY:,}
    Percent mined       : {round(circulating_coins/kaspa_constants.TOTAL_COIN_SUPPLY*100, 2)}%'''
    
    DEVFUND = lambda mining_addr_value, donation_addr_value : f'''
  =======================================================================
  Donation addresses:

    • {devfund_addresses.DONATION_ADDR}

  -----------------------------------------------------------------------
    Amount: {int(donation_addr_value):,} KAS 
  =======================================================================
  Mining addresses:

    • {devfund_addresses.MINING_ADDR}
    
  -----------------------------------------------------------------------
    Amount: {int(mining_addr_value):,} KAS
  =======================================================================
  TOTAL:    {int(mining_addr_value + donation_addr_value):,} KAS'''

    BALANCE = lambda balance : f'''
    {balance:,} KAS'''

    SUGGESTION = f'''
    Thanks for your suggestion!'''

    HASHRATE = lambda norm_hashrate : f'''
    Hashrate: {norm_hashrate}''' 
    
    CONSIDER_DONATION = f'''
    Please consider a donation:
    Kasper : {kasper_addresses.DONATION_ADDR}
    Devfund: {devfund_addresses.DONATION_ADDR}
    '''

    USEFUL_LINKS = '''
  Kaspa website: 
    https://kaspanet.org/
  Source code: 
    https://github.com/kaspanet/kaspad
  Quick start guide:
    tinyurl.com/ym8sbas7
  Node bootstrap:
    http://kaspadbase.com/
  Kaspa Wiki:
    https://kaspawiki.net/
  Kaspa for desktop (KDX):
    https://kdx.app/
  Web wallet:
    https://wallet.kaspanet.io/
  Paper wallet generator:
    https://github.com/svarogg/kaspaper/releases/latest 
  Faucet:
    https://faucet.kaspanet.io/
  Dashboards:
    http://kasboard-mainnet.daglabs-dev.com/
    http://kasboard.cbytensky.org/
  Livefeed:
    http://kgi-mainnet.daglabs-dev.com/
  Block explorers:
    http://katnip.cbytensky.org/
    http://blockexplorer.kaspanet.org/
  Cpu-miner:
    https://github.com/elichai/kaspa-miner/releases
  Gpu-miner:
    https://github.com/tmrlvi/kaspa-miner/releases'''

    MINING_CALC = lambda rewards : f'''
  KAS / sec   :  {rewards['secound']:,}
  KAS / min   :  {round(rewards['minute']):,}
  KAS / hour  :  {round(rewards['hour']):,}
  KAS / day   :  {round(rewards['day']):,}
  KAS / week  :  {round(rewards['week']):,}
  KAS / month :  {round(rewards['month']):,}
  KAS / year  :  {round(rewards['year']):,}'''

    DONATION_ADDRS = f'''
  Please consider a donation:
  • Kasperbot: 
    {kasper_addresses.DONATION_ADDR}
  • Devfund: 
    {devfund_addresses.DONATION_ADDR}'''