import spynnaker8 as p
import numpy
import math
import unittest
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

p.setup(1)
runtime=2500

#### Create Populations ####
# create input neurons
spike_times = [[5, 74, 92, 105, 117, 118, 138, 146, 164, 165, 167, 171, 183, 187, 670, 688, 701, 708, 727, 728, 748, 758, 760, 787, 794, 1233, 1234, 1259, 1346, 1362, 1393, 1411, 1437, 1443, 1450, 1467, 1469, 1470, 1498, 1517, 1521, 1539, 1547, 1568, 1574, 1805, 1813, 1840, 1876, 1896, 1915, 1948, 1970, 1988, 1989],
[24, 40, 59, 73, 81, 82, 94, 109, 125, 142, 153, 173, 194, 602, 605, 622, 635, 654, 664, 673, 704, 720, 742, 780, 795, 1205, 1209, 1210, 1244, 1302, 1310, 1314, 1331, 1334, 1358, 1386, 1402, 1432, 1441, 1541, 1547, 1591, 1803, 1812, 1824, 1827, 1836, 1891, 1893, 1895, 1921, 1931, 1933, 1958, 1959, 1992, 1994],
[12, 37, 72, 78, 92, 102, 115, 188, 199, 652, 668, 674, 686, 735, 754, 757, 771, 780, 786, 793, 795, 1227, 1267, 1275, 1292, 1310, 1314, 1326, 1330, 1332, 1358, 1360, 1380, 1419, 1441, 1449, 1464, 1467, 1517, 1518, 1583, 1810, 1841, 1865, 1914, 1922, 1947, 1950, 1963, 1965, 1985],
[32, 67, 69, 75, 100, 111, 126, 131, 147, 161, 183, 196, 600, 602, 636, 658, 697, 763, 770, 795, 1239, 1250, 1252, 1269, 1271, 1274, 1278, 1308, 1315, 1361, 1384, 1385, 1405, 1419, 1477, 1499, 1500, 1510, 1539, 1841, 1858, 1863, 1932, 1933, 1975, 1982, 1986],
[1, 2, 10, 11, 16, 17, 18, 48, 87, 90, 96, 110, 112, 130, 132, 160, 168, 179, 181, 195, 604, 630, 633, 682, 708, 760, 785, 1216, 1282, 1290, 1291, 1292, 1306, 1340, 1343, 1346, 1408, 1410, 1419, 1423, 1427, 1447, 1461, 1489, 1556, 1569, 1827, 1832, 1878, 1881, 1893, 1908, 1933, 1935, 1943, 1963, 1970, 1976, 1981, 1997],
[6, 61, 65, 72, 90, 111, 118, 159, 191, 621, 623, 644, 668, 678, 707, 717, 755, 785, 797, 1223, 1234, 1263, 1273, 1275, 1278, 1323, 1352, 1362, 1384, 1408, 1421, 1429, 1430, 1436, 1445, 1465, 1473, 1488, 1489, 1544, 1563, 1582, 1813, 1828, 1852, 1858, 1864, 1873, 1887, 1912, 1956, 1989],
[14, 21, 46, 90, 111, 139, 148, 155, 176, 179, 198, 199, 616, 642, 646, 686, 688, 738, 772, 774, 787, 789, 798, 1210, 1217, 1224, 1225, 1268, 1272, 1285, 1296, 1324, 1327, 1340, 1354, 1395, 1422, 1433, 1450, 1453, 1482, 1522, 1523, 1526, 1554, 1565, 1567, 1586, 1588, 1812, 1820, 1833, 1863, 1873, 1896, 1915, 1935, 1960, 1969, 1979],
[0, 13, 29, 60, 86, 96, 119, 152, 159, 184, 610, 618, 620, 634, 639, 649, 700, 727, 728, 764, 781, 1229, 1230, 1236, 1248, 1270, 1287, 1319, 1328, 1353, 1358, 1435, 1467, 1470, 1497, 1507, 1559, 1563, 1595, 1811, 1829, 1854, 1858, 1859, 1881, 1917, 1919, 1920, 1939, 1956, 1987, 1988],
[15, 22, 27, 31, 51, 58, 59, 60, 69, 82, 94, 129, 133, 138, 150, 185, 615, 674, 690, 700, 759, 770, 786, 787, 797, 1211, 1254, 1281, 1320, 1370, 1373, 1380, 1381, 1385, 1421, 1429, 1438, 1473, 1476, 1487, 1497, 1507, 1528, 1535, 1538, 1569, 1572, 1577, 1594, 1803, 1834, 1843, 1853, 1854, 1862, 1872, 1967, 1969],
[18, 23, 51, 93, 97, 125, 179, 182, 604, 618, 626, 641, 643, 645, 700, 702, 705, 714, 731, 735, 743, 754, 781, 1205, 1347, 1395, 1399, 1412, 1434, 1438, 1469, 1477, 1488, 1490, 1506, 1518, 1528, 1534, 1567, 1577, 1585, 1596, 1806, 1827, 1836, 1852, 1884, 1915, 1936, 1948, 1950, 1964, 1972, 1985],
[23, 28, 66, 85, 139, 180, 186, 196, 604, 653, 656, 676, 689, 691, 692, 718, 725, 731, 1214, 1223, 1230, 1232, 1242, 1247, 1248, 1304, 1318, 1347, 1378, 1383, 1387, 1396, 1469, 1487, 1490, 1504, 1526, 1554, 1596, 1806, 1822, 1830, 1840, 1854, 1873, 1884, 1899, 1907, 1924, 1928, 1951, 1966, 1980],
[15, 24, 25, 26, 71, 125, 199, 619, 658, 659, 667, 669, 672, 690, 704, 748, 752, 767, 769, 771, 793, 1203, 1226, 1236, 1269, 1298, 1311, 1315, 1335, 1365, 1419, 1427, 1431, 1452, 1463, 1483, 1506, 1546, 1551, 1593, 1839, 1862, 1890, 1927, 1952, 1962, 1968, 1970, 1978, 1984, 1989],
[7, 8, 31, 57, 89, 112, 114, 145, 148, 151, 199, 601, 606, 607, 629, 634, 644, 645, 693, 707, 723, 760, 773, 779, 1205, 1210, 1281, 1287, 1290, 1310, 1361, 1383, 1409, 1436, 1459, 1483, 1487, 1489, 1514, 1545, 1549, 1582, 1585, 1595, 1833, 1869, 1870, 1875, 1882, 1887, 1926, 1936, 1963, 1987, 1997],
[3, 7, 18, 51, 136, 144, 155, 180, 186, 188, 189, 649, 654, 657, 676, 709, 725, 726, 748, 786, 1225, 1263, 1345, 1368, 1373, 1426, 1428, 1432, 1448, 1473, 1481, 1515, 1538, 1544, 1546, 1560, 1580, 1594, 1823, 1836, 1875, 1878, 1879, 1909, 1945, 1962, 1963, 1970, 1978],
[25, 28, 32, 48, 52, 72, 76, 86, 91, 98, 112, 114, 124, 127, 135, 144, 152, 156, 679, 693, 698, 714, 731, 742, 769, 779, 797, 1202, 1232, 1239, 1256, 1259, 1284, 1311, 1323, 1373, 1392, 1406, 1407, 1488, 1499, 1502, 1514, 1524, 1540, 1570, 1575, 1588, 1807, 1820, 1822, 1828, 1843, 1863, 1885, 1887, 1888, 1894, 1908, 1919, 1927, 1943, 1959, 1962, 1979, 1994, 1996],
[19, 36, 56, 82, 95, 104, 106, 108, 109, 127, 144, 163, 194, 626, 643, 649, 655, 700, 703, 704, 727, 728, 753, 758, 762, 768, 775, 1227, 1232, 1274, 1311, 1363, 1400, 1449, 1535, 1541, 1556, 1563, 1572, 1574, 1579, 1584, 1801, 1822, 1830, 1928, 1976, 1987],
[2, 13, 35, 56, 73, 86, 106, 125, 182, 188, 189, 193, 601, 637, 657, 696, 704, 733, 758, 797, 1209, 1221, 1222, 1226, 1247, 1253, 1270, 1305, 1306, 1328, 1357, 1380, 1383, 1400, 1409, 1427, 1449, 1469, 1508, 1516, 1583, 1805, 1816, 1833, 1841, 1868, 1869, 1871, 1875, 1881, 1883, 1890, 1901, 1934, 1956, 1973, 1979],
[67, 68, 98, 121, 134, 614, 619, 636, 643, 675, 735, 1212, 1213, 1217, 1260, 1261, 1344, 1352, 1358, 1392, 1430, 1483, 1490, 1494, 1518, 1530, 1542, 1545, 1557, 1563, 1586, 1595, 1599, 1811, 1823, 1916, 1923, 1933, 1936],
[40, 57, 97, 100, 110, 118, 120, 166, 184, 601, 607, 609, 621, 632, 635, 645, 695, 704, 733, 746, 772, 1215, 1224, 1246, 1264, 1276, 1284, 1290, 1363, 1383, 1387, 1461, 1465, 1470, 1478, 1496, 1502, 1521, 1537, 1541, 1574, 1811, 1920, 1941, 1949, 1955, 1966, 1974],
[63, 71, 106, 109, 123, 129, 133, 155, 181, 610, 632, 670, 695, 711, 755, 769, 779, 783, 785, 794, 797, 1223, 1226, 1237, 1312, 1323, 1375, 1388, 1402, 1427, 1434, 1447, 1465, 1505, 1511, 1516, 1524, 1548, 1567, 1588, 1592, 1818, 1834, 1837, 1846, 1851, 1876, 1917, 1970, 1977],
[1, 2, 82, 88, 93, 130, 148, 151, 152, 175, 178, 183, 624, 647, 686, 693, 707, 711, 722, 1232, 1246, 1279, 1314, 1339, 1343, 1349, 1351, 1428, 1458, 1471, 1482, 1484, 1490, 1492, 1495, 1511, 1518, 1559, 1814, 1838, 1846, 1877, 1923, 1937, 1949, 1955, 1972, 1983, 1992, 1998],
[14, 15, 41, 128, 132, 177, 643, 670, 680, 686, 727, 759, 777, 1216, 1239, 1246, 1248, 1286, 1324, 1351, 1371, 1375, 1384, 1389, 1410, 1453, 1461, 1502, 1513, 1533, 1536, 1567, 1576, 1585, 1588, 1808, 1831, 1857, 1889, 1893, 1909, 1950, 1967, 1991],
[84, 93, 145, 156, 193, 195, 619, 656, 700, 707, 709, 1234, 1257, 1281, 1310, 1312, 1341, 1392, 1405, 1421, 1449, 1450, 1460, 1480, 1508, 1516, 1548, 1820, 1829, 1833, 1839, 1857, 1888, 1943, 1949, 1968, 1984, 1999],
[6, 17, 20, 32, 36, 43, 46, 91, 150, 171, 179, 603, 616, 634, 636, 654, 663, 687, 701, 704, 719, 740, 741, 744, 1212, 1230, 1235, 1238, 1263, 1272, 1284, 1300, 1326, 1361, 1425, 1474, 1501, 1530, 1842, 1851, 1854, 1860, 1882, 1884, 1907, 1910, 1912, 1914, 1944, 1980, 1991],
[17, 31, 72, 73, 98, 105, 108, 145, 169, 196, 600, 605, 614, 615, 667, 677, 683, 748, 771, 782, 795, 1213, 1275, 1308, 1311, 1340, 1369, 1422, 1437, 1444, 1467, 1468, 1476, 1504, 1507, 1513, 1516, 1528, 1546, 1558, 1576, 1591, 1807, 1810, 1824, 1826, 1833, 1840, 1860, 1900, 1906, 1964, 1973, 1976],
[293, 335, 401, 403, 422, 449, 451, 467, 475, 488, 492, 494, 523, 542, 564, 568, 824, 844, 854, 857, 863, 864, 874, 889, 954, 999, 1053, 1070, 1111, 1152, 1181, 1184, 1199, 1610, 1629, 1633, 1646, 1734, 1758, 2071, 2082, 2083, 2101, 2105, 2116, 2132, 2149, 2175, 2196],
[236, 246, 267, 297, 332, 343, 349, 355, 366, 390, 404, 444, 451, 456, 507, 510, 513, 519, 521, 534, 557, 560, 570, 572, 802, 804, 809, 815, 820, 841, 845, 865, 878, 896, 923, 931, 965, 973, 988, 990, 991, 1004, 1023, 1035, 1044, 1058, 1062, 1090, 1100, 1121, 1170, 1172, 1631, 1635, 1652, 1694, 1738, 1746, 1754, 1768, 1789, 2059, 2063, 2075, 2085, 2090, 2095, 2116, 2134, 2174, 2178, 2194],
[203, 214, 223, 240, 242, 303, 331, 341, 386, 387, 406, 408, 411, 446, 452, 538, 548, 554, 568, 569, 589, 593, 802, 803, 813, 816, 845, 847, 868, 888, 893, 906, 935, 961, 973, 994, 1008, 1012, 1066, 1071, 1075, 1106, 1107, 1111, 1122, 1143, 1164, 1177, 1195, 1615, 1621, 1683, 1713, 1739, 1744, 2060, 2062, 2076, 2106, 2121, 2137, 2146, 2172, 2178],
[207, 225, 232, 243, 251, 284, 286, 295, 298, 304, 319, 332, 333, 355, 370, 434, 445, 451, 455, 508, 524, 564, 583, 803, 816, 821, 858, 864, 865, 870, 889, 899, 900, 904, 958, 1004, 1022, 1035, 1046, 1068, 1080, 1089, 1099, 1102, 1118, 1120, 1181, 1606, 1631, 1638, 1668, 1683, 1705, 1710, 1726, 1750, 1798, 2031, 2059, 2075, 2087, 2093, 2100, 2124, 2140, 2153, 2175, 2185, 2187, 2196],
[231, 242, 254, 268, 272, 289, 346, 368, 384, 398, 403, 407, 416, 444, 447, 463, 472, 503, 539, 546, 559, 561, 563, 823, 941, 964, 988, 999, 1025, 1030, 1037, 1040, 1050, 1052, 1075, 1137, 1140, 1142, 1155, 1185, 1188, 1193, 1636, 1647, 1675, 1732, 1740, 1775, 1776, 1788, 1799, 2008, 2015, 2019, 2039, 2043, 2045, 2054, 2090, 2103, 2116, 2134, 2147, 2158, 2161, 2163],
[206, 273, 294, 331, 361, 364, 397, 403, 412, 428, 434, 441, 459, 460, 463, 478, 482, 527, 538, 539, 543, 867, 887, 893, 917, 923, 953, 962, 989, 1007, 1049, 1051, 1059, 1072, 1085, 1144, 1149, 1158, 1160, 1177, 1179, 1626, 1642, 1648, 1654, 1657, 1666, 1667, 1682, 1684, 1697, 1698, 1705, 1772, 1786, 2000, 2057, 2088, 2119, 2127, 2137, 2140, 2154, 2178],
[219, 244, 308, 310, 328, 329, 337, 342, 345, 370, 385, 416, 449, 472, 480, 486, 489, 519, 524, 525, 529, 535, 550, 557, 805, 827, 837, 871, 873, 882, 893, 903, 904, 929, 935, 955, 972, 1036, 1105, 1106, 1112, 1118, 1127, 1154, 1178, 1179, 1625, 1638, 1681, 1685, 1694, 1724, 1764, 1799, 2061, 2066, 2079, 2094, 2117, 2150, 2156, 2163, 2188],
[202, 209, 241, 243, 279, 297, 328, 336, 381, 384, 413, 423, 439, 454, 477, 503, 511, 512, 520, 803, 807, 812, 829, 849, 867, 868, 869, 872, 878, 926, 936, 952, 989, 999, 1013, 1019, 1026, 1029, 1048, 1062, 1068, 1096, 1132, 1134, 1143, 1605, 1611, 1659, 1669, 1675, 1683, 1710, 1713, 1714, 1747, 1757, 1760, 1774, 1787, 1790, 1794, 1795, 2004, 2005, 2018, 2066, 2078, 2106, 2155, 2157, 2159, 2174, 2182, 2197],
[245, 253, 290, 306, 310, 313, 318, 320, 324, 362, 393, 445, 456, 459, 483, 504, 506, 517, 535, 567, 578, 588, 593, 831, 850, 893, 906, 933, 947, 955, 969, 985, 1005, 1025, 1040, 1043, 1045, 1057, 1063, 1080, 1099, 1113, 1143, 1168, 1169, 1176, 1658, 1750, 1760, 1764, 1794, 2008, 2012, 2045, 2046, 2056, 2084, 2092, 2106, 2110, 2113, 2122, 2137, 2191],
[203, 212, 218, 269, 292, 309, 331, 333, 345, 357, 434, 445, 450, 480, 500, 524, 552, 557, 588, 820, 826, 856, 857, 920, 964, 965, 1045, 1096, 1108, 1126, 1147, 1154, 1165, 1185, 1604, 1607, 1687, 1691, 1702, 1706, 1713, 1748, 1763, 1787, 1792, 1793, 2006, 2009, 2049, 2070, 2072, 2125, 2143, 2183, 2184, 2194],
[206, 222, 236, 241, 247, 250, 339, 375, 462, 493, 496, 506, 508, 524, 525, 533, 577, 584, 847, 864, 903, 922, 923, 940, 946, 953, 976, 1003, 1073, 1079, 1084, 1137, 1147, 1613, 1640, 1646, 1661, 1712, 1724, 1741, 1768, 1778, 2020, 2023, 2054, 2084, 2103, 2106, 2109, 2119, 2124, 2128, 2161, 2173, 2180],
[214, 230, 249, 282, 290, 321, 331, 387, 394, 424, 465, 469, 478, 504, 523, 533, 546, 570, 808, 838, 841, 893, 930, 973, 987, 1020, 1060, 1065, 1092, 1099, 1111, 1135, 1182, 1606, 1652, 1655, 1667, 1669, 1674, 1696, 1723, 1730, 1739, 1745, 1787, 2026, 2045, 2180],
[209, 234, 244, 248, 256, 261, 299, 318, 360, 365, 367, 406, 424, 434, 595, 802, 823, 867, 904, 926, 962, 972, 975, 983, 1054, 1068, 1078, 1115, 1132, 1144, 1198, 1611, 1632, 1640, 1642, 1670, 1700, 1718, 1721, 1727, 1750, 1770, 1772, 1783, 2029, 2051, 2134, 2138, 2166, 2178],
[224, 229, 238, 283, 302, 409, 431, 432, 441, 488, 494, 550, 853, 858, 869, 918, 926, 927, 932, 935, 936, 991, 1031, 1037, 1059, 1070, 1103, 1110, 1123, 1138, 1165, 1616, 1617, 1661, 1688, 1722, 1738, 1752, 1776, 1790, 2057, 2085, 2091, 2105, 2123, 2174, 2183, 2191],
[201, 239, 278, 333, 346, 375, 410, 426, 431, 442, 462, 501, 516, 524, 532, 535, 541, 801, 829, 860, 863, 866, 867, 875, 895, 992, 1008, 1033, 1106, 1109, 1113, 1118, 1131, 1173, 1183, 1185, 1619, 1641, 1642, 1643, 1680, 1698, 1738, 1763, 1768, 2009, 2026, 2046, 2113, 2148, 2150, 2151, 2185],
[228, 233, 247, 254, 265, 267, 294, 306, 314, 352, 358, 363, 364, 385, 413, 419, 463, 482, 487, 505, 567, 576, 590, 831, 832, 906, 917, 949, 990, 1028, 1056, 1079, 1087, 1101, 1107, 1159, 1170, 1181, 1182, 1188, 1194, 1608, 1617, 1654, 1664, 1674, 1683, 1723, 1724, 1759, 2011, 2022, 2064, 2078, 2083, 2102, 2120, 2144, 2174],
[225, 234, 237, 254, 265, 270, 273, 275, 283, 292, 325, 349, 388, 398, 428, 443, 471, 474, 482, 483, 489, 495, 501, 535, 550, 564, 572, 574, 575, 598, 842, 846, 859, 864, 879, 882, 935, 954, 957, 978, 1009, 1016, 1033, 1082, 1103, 1104, 1106, 1113, 1117, 1136, 1184, 1190, 1624, 1658, 1669, 1672, 1676, 1680, 1705, 1742, 1744, 1752, 1757, 1768, 1773, 1798, 2017, 2027, 2079, 2092, 2100, 2160, 2167],
[216, 219, 238, 241, 244, 248, 254, 265, 304, 331, 356, 363, 403, 420, 441, 460, 473, 481, 519, 549, 848, 850, 930, 947, 954, 958, 966, 1038, 1060, 1095, 1096, 1127, 1136, 1156, 1167, 1186, 1198, 1623, 1677, 1703, 1715, 1741, 1753, 1755, 1761, 1783, 1788, 1794, 2013, 2057, 2068, 2104, 2167, 2176, 2198],
[203, 258, 278, 300, 316, 330, 381, 386, 393, 396, 416, 460, 472, 474, 477, 486, 537, 539, 542, 552, 555, 814, 838, 842, 878, 926, 941, 967, 978, 1030, 1047, 1184, 1186, 1601, 1606, 1607, 1678, 1714, 1746, 2001, 2018, 2041, 2060, 2062, 2142, 2172, 2180, 2188, 2194, 2195, 2196],
[245, 250, 268, 282, 311, 403, 417, 424, 447, 454, 456, 516, 521, 537, 541, 555, 564, 583, 806, 819, 850, 894, 939, 988, 1002, 1016, 1032, 1062, 1072, 1119, 1126, 1137, 1143, 1146, 1175, 1193, 1627, 1655, 1680, 1691, 1731, 1732, 1753, 1785, 2005, 2021, 2067, 2078, 2097, 2118, 2142, 2164, 2183],
[209, 215, 216, 244, 253, 262, 272, 317, 325, 327, 357, 361, 373, 396, 399, 421, 429, 442, 450, 514, 557, 561, 582, 590, 809, 838, 858, 948, 967, 999, 1027, 1033, 1066, 1083, 1097, 1101, 1127, 1134, 1135, 1150, 1186, 1609, 1698, 1728, 1765, 1783, 1789, 1793, 2032, 2058, 2126, 2154, 2161, 2176],
[227, 233, 237, 266, 276, 298, 308, 345, 355, 397, 400, 436, 438, 451, 467, 506, 521, 546, 579, 581, 587, 826, 843, 864, 909, 915, 931, 932, 937, 972, 1064, 1078, 1085, 1089, 1112, 1156, 1170, 1623, 1628, 1631, 1636, 1686, 1713, 1730, 1773, 1775, 2014, 2034, 2089, 2092, 2128],
[214, 224, 237, 244, 246, 264, 277, 307, 351, 379, 413, 439, 452, 464, 479, 480, 490, 515, 544, 579, 593, 833, 883, 922, 949, 966, 989, 990, 1097, 1129, 1183, 1185, 1186, 1188, 1191, 1608, 1628, 1662, 1663, 1682, 1709, 1711, 1714, 1742, 1763, 1777, 1791, 1792, 2001, 2011, 2021, 2022, 2032, 2047, 2054, 2061, 2064, 2082, 2083, 2106, 2115, 2127],
[207, 210, 219, 221, 231, 232, 242, 245, 278, 294, 327, 341, 382, 411, 512, 538, 541, 564, 569, 572, 826, 836, 857, 879, 930, 931, 935, 952, 971, 972, 1013, 1047, 1049, 1079, 1094, 1117, 1135, 1138, 1158, 1177, 1186, 1601, 1638, 1643, 1659, 1661, 1669, 1674, 1678, 1701, 1711, 1772, 1788, 2033, 2036, 2062, 2067, 2106, 2118, 2164, 2183, 2191, 2192],
[287, 321, 341, 364, 421, 438, 448, 449, 458, 484, 501, 552, 580, 587, 588, 810, 829, 834, 836, 842, 844, 848, 960, 966, 984, 1005, 1035, 1045, 1049, 1063, 1135, 1153, 1173, 1185, 1190, 1609, 1648, 1664, 1672, 1693, 1708, 1738, 1747, 1761, 1781, 2019, 2022, 2043, 2070, 2078, 2124, 2146, 2159, 2180, 2188, 2192, 2198],
[1, 16, 74, 79, 87, 122, 134, 136, 156, 184, 195],
[15, 21, 30, 37, 79, 157, 168, 187],
[23, 25, 56, 76, 88, 111, 124, 137, 163],
[22, 35, 37, 38, 54, 56, 84, 85, 87, 88, 112, 132, 176, 196],
[35, 48, 73, 80, 102, 104, 110, 133, 174, 179, 198],
[37, 55, 59, 62, 66, 82, 85, 86, 146, 156],
[16, 70, 73, 111, 134, 137, 156, 175, 179, 182, 193],
[0, 36, 78, 79, 81, 101, 115, 120, 126, 127, 133, 145, 154],
[1, 54, 63, 138, 182, 191],
[31, 68, 70, 84, 98, 119, 121, 136, 139, 140, 173, 187],
[24, 53, 70, 78, 90, 147, 165, 193],
[4, 6, 10, 37, 85, 110, 113, 114, 119, 132, 162, 177, 186],
[10, 32, 34, 36, 47, 69, 101, 145, 147, 155],
[0, 40, 54, 55, 56, 58, 65, 66, 122, 128, 132, 139, 176, 188],
[79, 92, 104, 116, 117, 119, 138, 153, 156, 160, 170],
[4, 13, 27, 101, 121, 130, 165],
[0, 8, 30, 61, 68, 88, 89, 93, 109, 141, 151, 176],
[5, 12, 19, 21, 22, 24, 28, 44, 52, 66, 100, 103, 115, 125, 126, 133, 160, 171],
[23, 31, 38, 69, 82, 96, 102, 109, 115, 129, 136, 138, 180, 189, 191],
[4, 14, 19, 172, 174, 175, 196],
[16, 24, 38, 62, 87, 100, 109, 134, 150, 163, 165, 174, 186],
[29, 68, 91, 100, 150, 172, 190],
[0, 1, 3, 9, 35, 49, 54, 55, 64, 68, 73, 98, 103, 137, 195],
[13, 14, 39, 55, 70, 100, 139, 167, 186, 191],
[65, 72, 93, 110, 182],
[2205, 2211, 2213, 2216, 2217, 2253, 2302, 2398],
[2222, 2275, 2282, 2311, 2327, 2336, 2343, 2358, 2365, 2368],
[2206, 2215, 2249, 2289, 2338, 2374, 2397],
[2250, 2270, 2276, 2279, 2369, 2378],
[2201, 2211, 2216, 2219, 2270, 2280, 2317, 2323, 2329, 2337, 2375, 2383, 2389],
[2250, 2293, 2295, 2296, 2316, 2360, 2380, 2383],
[2207, 2213, 2291, 2310, 2312, 2328, 2339, 2357, 2374, 2383],
[2214, 2230, 2239, 2247, 2248, 2269, 2287, 2289, 2303, 2337, 2344, 2378, 2385, 2386],
[2258, 2260, 2286, 2288, 2291, 2323, 2377, 2378, 2379],
[2241, 2275, 2293, 2324, 2326, 2376, 2394, 2397],
[2209, 2217, 2235, 2258, 2282, 2304, 2313, 2330],
[2219, 2221, 2241, 2275, 2278, 2279, 2283, 2296, 2328, 2346, 2349, 2355, 2384, 2386],
[2223, 2319, 2352, 2358, 2378, 2382, 2384, 2391],
[2216, 2244, 2268, 2274, 2304, 2305, 2322, 2325, 2328, 2341, 2354, 2367, 2373, 2393],
[2239, 2271, 2284, 2286, 2289, 2298, 2310, 2316, 2321, 2325, 2328, 2348, 2364, 2373, 2374, 2390],
[2249, 2268, 2270, 2271, 2282, 2286, 2288, 2296, 2313, 2377],
[2212, 2228, 2338, 2359],
[2208, 2225, 2237, 2245, 2250, 2263, 2326, 2354],
[2213, 2267, 2279, 2289, 2301, 2390, 2398],
[2230, 2241, 2244, 2255, 2284, 2286, 2308, 2320, 2340, 2341, 2351, 2362, 2366, 2383, 2385],
[2219, 2229, 2238, 2252, 2284, 2298, 2301, 2313, 2322, 2343, 2354, 2369],
[2215, 2240, 2311, 2312, 2321, 2345, 2350, 2375],
[2212, 2218, 2259, 2266, 2280, 2296, 2308, 2313, 2316, 2322, 2329, 2333, 2353, 2363, 2370, 2373, 2384, 2392, 2393, 2397, 2398],
[2209, 2229, 2230, 2234, 2263, 2280, 2315, 2351, 2387],
[2200, 2223, 2254, 2277, 2377, 2383, 2388, 2392]]

pop_input = p.Population(100, p.SpikeSourceArray,
                        {'spike_times': spike_times}, label="input")

# create hidden neurons
hidden_neuron_params = {
    'tau_m': 20.0,
    'cm': 20, # Updated to suit tau_m of 20 and make membrane resistance 1
    'v_rest': 0.0,
#     "i_offset": 200, # dc current
    'thresh_B': 10.0,
    'thresh_b_0': 10,
    'thresh_tau_a': 1200,
    'thresh_beta': 1.7,
    'tau_refrac':3
    }

pop_hidden = p.Population(2,
            p.extra_models.IFCurrDeltaGrazAdaptive(**hidden_neuron_params),
            label='hidden')


# # create output neurons
# output_neuron_params = {
#     'tau_m': 20.0,
#     'cm': 1.0,
#     'v_rest': -65.0,
#     'v_reset': -65.0,
#     "i_offset":0.8, # dc current
#     'v_thresh': -50.0,
#     'v_thresh_resting': -50,
#     'v_thresh_tau': 700,
#     'v_thresh_adaptation': 2,
#     }
#
# pop_output = p.Population(2, p.IF_curr_exp(**output_neuron_paramters),
#                           label='output')

#### Create synaptic connections ####
IH_conn_list_exc=[[0, 0, 0.002, 2],
[1, 0, 0.002, 0],
[2, 0, 0.002, 8],
[3, 0, 0.002, 0],
[4, 0, 0.002, 8],
[5, 0, 0.002, 2],
[6, 0, 0.002, 6],
[7, 0, 0.002, 0],
[8, 0, 0.002, 5],
[9, 0, 0.002, 7],
[10, 0, 0.002, 7],
[11, 0, 0.002, 2],
[12, 0, 0.002, 1],
[13, 0, 0.002, 1],
[14, 0, 0.002, 0],
[15, 0, 0.002, 4],
[16, 0, 0.002, 6],
[17, 0, 0.002, 8],
[18, 0, 0.002, 8],
[19, 0, 0.002, 3],
[20, 0, 0.002, 0],
[21, 0, 0.002, 5],
[22, 0, 0.002, 9],
[23, 0, 0.002, 2],
[24, 0, 0.002, 0],
[50, 0, 0.1, 2],
[51, 0, 0.1, 1],
[52, 0, 0.1, 5],
[53, 0, 0.1, 6],
[54, 0, 0.1, 4],
[55, 0, 0.1, 6],
[56, 0, 0.1, 1],
[57, 0, 0.1, 4],
[58, 0, 0.1, 3],
[59, 0, 0.1, 6],
[60, 0, 0.1, 2],
[61, 0, 0.1, 0],
[62, 0, 0.1, 1],
[63, 0, 0.1, 0],
[64, 0, 0.1, 6],
[65, 0, 0.1, 0],
[66, 0, 0.1, 6],
[67, 0, 0.1, 0],
[68, 0, 0.1, 0],
[69, 0, 0.1, 8],
[70, 0, 0.1, 1],
[71, 0, 0.1, 7],
[72, 0, 0.1, 3],
[73, 0, 0.1, 7],
[74, 0, 0.1, 0],
[75, 0, 0.1, 5],
[76, 0, 0.1, 5],
[77, 0, 0.1, 4],
[78, 0, 0.1, 1],
[79, 0, 0.1, 8],
[80, 0, 0.1, 2],
[81, 0, 0.1, 6],
[82, 0, 0.1, 7],
[83, 0, 0.1, 5],
[84, 0, 0.1, 9],
[85, 0, 0.1, 8],
[86, 0, 0.1, 5],
[87, 0, 0.1, 0],
[88, 0, 0.1, 3],
[89, 0, 0.1, 3],
[90, 0, 0.1, 9],
[91, 0, 0.1, 8],
[92, 0, 0.1, 5],
[93, 0, 0.1, 7],
[94, 0, 0.1, 0],
[95, 0, 0.1, 9],
[96, 0, 0.1, 0],
[97, 0, 0.1, 4],
[98, 0, 0.1, 3],
[99, 0, 0.1, 2],
[25, 1, 0.002, 7],
[26, 1, 0.002, 4],
[27, 1, 0.002, 1],
[28, 1, 0.002, 9],
[29, 1, 0.002, 3],
[30, 1, 0.002, 5],
[31, 1, 0.002, 4],
[32, 1, 0.002, 0],
[33, 1, 0.002, 7],
[34, 1, 0.002, 0],
[35, 1, 0.002, 0],
[36, 1, 0.002, 4],
[37, 1, 0.002, 4],
[38, 1, 0.002, 4],
[39, 1, 0.002, 9],
[40, 1, 0.002, 8],
[41, 1, 0.002, 3],
[42, 1, 0.002, 7],
[43, 1, 0.002, 1],
[44, 1, 0.002, 7],
[45, 1, 0.002, 0],
[46, 1, 0.002, 6],
[47, 1, 0.002, 7],
[48, 1, 0.002, 2],
[49, 1, 0.002, 3],
[50, 1, 0.1, 5],
[51, 1, 0.1, 8],
[52, 1, 0.1, 3],
[53, 1, 0.1, 3],
[54, 1, 0.1, 4],
[55, 1, 0.1, 4],
[56, 1, 0.1, 9],
[57, 1, 0.1, 8],
[58, 1, 0.1, 5],
[59, 1, 0.1, 0],
[60, 1, 0.1, 1],
[61, 1, 0.1, 1],
[62, 1, 0.1, 0],
[63, 1, 0.1, 8],
[64, 1, 0.1, 9],
[65, 1, 0.1, 3],
[66, 1, 0.1, 3],
[67, 1, 0.1, 5],
[68, 1, 0.1, 2],
[69, 1, 0.1, 9],
[70, 1, 0.1, 1],
[71, 1, 0.1, 1],
[72, 1, 0.1, 7],
[73, 1, 0.1, 5],
[74, 1, 0.1, 8],
[75, 1, 0.1, 7],
[76, 1, 0.1, 7],
[77, 1, 0.1, 0],
[78, 1, 0.1, 0],
[79, 1, 0.1, 6],
[80, 1, 0.1, 5],
[81, 1, 0.1, 1],
[82, 1, 0.1, 4],
[83, 1, 0.1, 9],
[84, 1, 0.1, 3],
[85, 1, 0.1, 8],
[86, 1, 0.1, 4],
[87, 1, 0.1, 5],
[88, 1, 0.1, 5],
[89, 1, 0.1, 8],
[90, 1, 0.1, 2],
[91, 1, 0.1, 9],
[92, 1, 0.1, 9],
[93, 1, 0.1, 9],
[94, 1, 0.1, 8],
[95, 1, 0.1, 0],
[96, 1, 0.1, 0],
[97, 1, 0.1, 8],
[98, 1, 0.1, 0],
[99, 1, 0.1, 5]]

IH_conn_list_inh=[[0, 1, -0.1, 5],
[1, 1, -0.1, 5],
[2, 1, -0.1, 6],
[3, 1, -0.1, 6],
[4, 1, -0.1, 5],
[5, 1, -0.1, 0],
[6, 1, -0.1, 3],
[7, 1, -0.1, 5],
[8, 1, -0.1, 3],
[9, 1, -0.1, 8],
[10, 1, -0.1, 2],
[11, 1, -0.1, 3],
[12, 1, -0.1, 0],
[13, 1, -0.1, 7],
[14, 1, -0.1, 8],
[15, 1, -0.1, 7],
[16, 1, -0.1, 8],
[17, 1, -0.1, 3],
[18, 1, -0.1, 2],
[19, 1, -0.1, 0],
[20, 1, -0.1, 0],
[21, 1, -0.1, 6],
[22, 1, -0.1, 5],
[23, 1, -0.1, 2],
[24, 1, -0.1, 0],
[25, 0, -0.1, 4],
[26, 0, -0.1, 9],
[27, 0, -0.1, 6],
[28, 0, -0.1, 2],
[29, 0, -0.1, 7],
[30, 0, -0.1, 5],
[31, 0, -0.1, 8],
[32, 0, -0.1, 8],
[33, 0, -0.1, 2],
[34, 0, -0.1, 1],
[35, 0, -0.1, 7],
[36, 0, -0.1, 7],
[37, 0, -0.1, 5],
[38, 0, -0.1, 0],
[39, 0, -0.1, 9],
[40, 0, -0.1, 9],
[41, 0, -0.1, 8],
[42, 0, -0.1, 7],
[43, 0, -0.1, 2],
[44, 0, -0.1, 4],
[45, 0, -0.1, 4],
[46, 0, -0.1, 2],
[47, 0, -0.1, 2],
[48, 0, -0.1, 6],
[49, 0, -0.1, 1]]

HH_conn_list_exc=[
    [0, 0, 0.0, 4],
    [1, 1, 0.0, 5]
    ]
HH_conn_list_inh=[
    [1, 0, 1.0, 1],
    [0, 1, 1.0, 0]
    ]

scalar = 1000
for i in IH_conn_list_exc:
    i[2] = i[2]*scalar
    i[3] = i[3]+1

for i in IH_conn_list_inh:
    i[2] = i[2]*-scalar
    i[3] = i[3]+1

for i in HH_conn_list_exc:
    i[2] = i[2]*scalar
    i[3] = i[3]+1

for i in HH_conn_list_inh:
    i[2] = i[2]*scalar
    i[3] = i[3]+1

# Create Input-to-Hidden projections
synapse_inp_to_hidden_exc = p.Projection(
    pop_input, pop_hidden, p.FromListConnector(IH_conn_list_exc),
    p.StaticSynapse(), receptor_type="excitatory")
synapse_inp_to_hidden_inh = p.Projection(
    pop_input, pop_hidden, p.FromListConnector(IH_conn_list_inh),
    p.StaticSynapse(), receptor_type="inhibitory")

# Create Hidden-to-Hidden (recurrent) projections
synapse_hidden_to_hidden_exc = p.Projection(
    pop_hidden, pop_hidden, p.FromListConnector(HH_conn_list_exc),
    p.StaticSynapse(), receptor_type="excitatory")

synapse_hidden_to_hidden_inh = p.Projection(
    pop_hidden, pop_hidden, p.FromListConnector(HH_conn_list_inh),
    p.StaticSynapse(), receptor_type="inhibitory")

# # Create Hidden-to-Output projections
# synapse_hidden_to_hidden = p.Projection(
#     pop_hidden, pop_output, p.FromListConnector(),
#     p.StaticSynapse(), receptor_type="excitatory")


#### Run Simulation ####
pop_input.record('all')
pop_hidden.record("all")
p.run(runtime)

pre_spikes = pop_input.get_data('spikes')
hidden_data = pop_hidden.get_data()

# Plot
Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(pre_spikes.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    # plot data for postsynaptic neuron
    Panel(hidden_data.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)),
    Panel(hidden_data.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)),
    Panel(hidden_data.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[pop_hidden.label], yticks=True, xlim=(0, runtime)),
    Panel(hidden_data.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
)


n=1
for n in [0,1]:

    for i in hidden_data.segments[0].spiketrains[0]:
        print i.magnitude

    print "\n\n\n\n\n"
    print "*************************************"

    for i in hidden_data.segments[0].filter(name='gsyn_inh')[0]:
        print i.magnitude[n]

    print "\n\n\n\n\n"
    print "*************************************"

    for i in hidden_data.segments[0].filter(name='v')[0]:
        print i.magnitude[n]

    print "\n\n\n\n\n"
    print "*************************************"

    for i in hidden_data.segments[0].filter(name='gsyn_exc')[0]:
        print i.magnitude[n]




plt.show()
p.end()

