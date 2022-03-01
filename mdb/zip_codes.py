"""ZIP codes library."""

from itertools import chain
from typing import Union

from mdb.enumerations import State


__all__ = ['RANGES', 'STATES', 'ZIP_CODES', 'get_state']


# Mapping taken from: https://cebus.net/de/plz-bundesland.htm
RANGES = {
    State.SN: [
        range(1001, 1936),
        range(2601, 2999),
        range(4001, 4579),
        range(4641, 4889),
        range(7919, 7919),
        range(7919, 7919),
        range(7951, 7951),
        range(7952, 7952),
        range(7982, 7982),
        range(7985, 7985),
        range(8001, 9669)
    ],
    State.BB: [
        range(1941, 1998),
        range(3001, 3253),
        range(4891, 4938),
        range(14401, 14715),
        range(14723, 16949),
        range(17258, 17258),
        range(17261, 17291),
        range(17309, 17309),
        range(17321, 17321),
        range(17326, 17326),
        range(17335, 17335),
        range(17337, 17337),
        range(19307, 19357)
    ],
    State.TH: [
        range(4581, 4639),
        range(6551, 6578),
        range(7301, 7919),
        range(7919, 7919),
        range(7920, 7950),
        range(7952, 7952),
        range(7953, 7980),
        range(7985, 7985),
        range(7985, 7989),
        range(36401, 36469),
        range(37301, 37359),
        range(96501, 96529),
        range(98501, 99998)
    ],
    State.ST: [
        range(6001, 6548),
        range(6601, 6928),
        range(14715, 14715),
        range(29401, 29416),
        range(38481, 38489),
        range(38801, 39649)
    ],
    State.BE: [
        range(10001, 14330)
    ],
    State.MV: [
        range(17001, 17256),
        range(17258, 17259),
        range(17301, 17309),
        range(17309, 17321),
        range(17321, 17322),
        range(17328, 17331),
        range(17335, 17335),
        range(17337, 19260),
        range(19273, 19273),
        range(19273, 19306),
        range(19357, 19417),
        range(23921, 23999)
    ],
    State.NI: [
        range(19271, 19273),
        range(21202, 21449),
        range(21522, 21522),
        range(21601, 21789),
        range(26001, 27478),
        range(27607, 27809),
        range(28784, 29399),
        range(29431, 31868),
        range(34331, 34353),
        range(34355, 34355),
        range(37001, 37194),
        range(37197, 37199),
        range(37401, 37649),
        range(37689, 37691),
        range(37697, 38479),
        range(38501, 38729),
        range(48442, 48465),
        range(48478, 48480),
        range(48486, 48488),
        range(48497, 48531),
        range(49001, 49459),
        range(49551, 49849)
    ],
    State.HH: [
        range(20001, 21037),
        range(21039, 21170),
        range(22001, 22113),
        range(22115, 22143),
        range(22145, 22145),
        range(22147, 22786),
        range(27499, 27499)
    ],
    State.SH: [
        range(21039, 21039),
        range(21451, 21521),
        range(21524, 21529),
        range(22113, 22113),
        range(22145, 22145),
        range(22145, 22145),
        range(22801, 23919),
        range(24001, 25999),
        range(27483, 27498)
    ],
    State.HB: [
        range(27501, 27580),
        range(28001, 28779)
    ],
    State.NW: [
        range(32001, 33829),
        range(34401, 34439),
        range(37651, 37688),
        range(37692, 37696),
        range(40001, 48432),
        range(48466, 48477),
        range(48481, 48485),
        range(48489, 48496),
        range(48541, 48739),
        range(49461, 49549),
        range(50101, 51597),
        range(51601, 53359),
        range(53581, 53604),
        range(53621, 53949),
        range(57001, 57489),
        range(58001, 59966),
        range(59969, 59969)
    ],
    State.HE: [
        range(34001, 34329),
        range(34355, 34355),
        range(34356, 34399),
        range(34441, 36399),
        range(37194, 37195),
        range(37201, 37299),
        range(55240, 55252),
        range(59969, 59969),
        range(60001, 63699),
        range(63776, 63776),
        range(64201, 64753),
        range(64754, 65326),
        range(65327, 65391),
        range(65392, 65556),
        range(65583, 65620),
        range(65627, 65627),
        range(65701, 65936),
        range(68501, 68519),
        range(68601, 68649),
        range(69235, 69239),
        range(69430, 69431),
        range(69434, 69434),
        range(69479, 69488),
        range(69503, 69509),
        range(69515, 69518)
    ],
    State.RP: [
        range(51598, 51598),
        range(53401, 53579),
        range(53614, 53619),
        range(54181, 55239),
        range(55253, 56869),
        range(57501, 57648),
        range(65326, 65326),
        range(65391, 65391),
        range(65558, 65582),
        range(65621, 65626),
        range(65629, 65629),
        range(66461, 66509),
        range(66841, 67829),
        range(76711, 76891)
    ],
    State.BY: [
        range(63701, 63774),
        range(63776, 63928),
        range(63930, 63939),
        range(74594, 74594),
        range(80001, 87490),
        range(87493, 87561),
        range(87571, 87789),
        range(88101, 88146),
        range(88147, 88179),
        range(89081, 89081),
        range(89087, 89087),
        range(89201, 89449),
        range(90001, 96489),
        range(97001, 97859),
        range(97888, 97892),
        range(97896, 97896),
        range(97901, 97909)
    ],
    State.BW: [
        range(63928, 63928),
        range(64754, 64754),
        range(68001, 68312),
        range(68520, 68549),
        range(68701, 69234),
        range(69240, 69429),
        range(69434, 69434),
        range(69435, 69469),
        range(69489, 69502),
        range(69510, 69514),
        range(70001, 74592),
        range(74594, 76709),
        range(77601, 79879),
        range(88001, 88099),
        range(88147, 88147),
        range(88181, 89079),
        range(89081, 89085),
        range(89090, 89198),
        range(89501, 89619),
        range(97861, 97877),
        range(97893, 97896),
        range(97897, 97900),
        range(97911, 97999)
    ],
    State.SL: [
        range(66001, 66459),
        range(66511, 66839)
    ]
}

STATES = {
    state: set(chain.from_iterable(zip_code_ranges))
    for state, zip_code_ranges in RANGES.items()
}

ZIP_CODES = {
    zip_code: state for state, zip_codes in STATES.items()
    for zip_code in zip_codes
}


def get_state(zip_code: Union[str, int]) -> State:
    """Returns a state by the given zip code."""

    if isinstance(zip_code, str):
        return get_state(int(zip_code))

    return ZIP_CODES[zip_code]
