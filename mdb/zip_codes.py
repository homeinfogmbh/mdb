"""ZIP codes library."""

from itertools import chain
from typing import Union

from mdb.enumerations import State


__all__ = ['RANGES', 'STATES', 'ZIP_CODES', 'get_state']


def zip_code_range(start: int, end: int) -> range:
    """Range of zip codes which includes the end."""

    return range(start, end + 1)


# Mapping taken from: https://cebus.net/de/plz-bundesland.htm
RANGES = {
    State.SN: [
        zip_code_range(1001, 1936),
        zip_code_range(2601, 2999),
        zip_code_range(4001, 4579),
        zip_code_range(4641, 4889),
        zip_code_range(7919, 7919),
        zip_code_range(7919, 7919),
        zip_code_range(7951, 7951),
        zip_code_range(7952, 7952),
        zip_code_range(7982, 7982),
        zip_code_range(7985, 7985),
        zip_code_range(8001, 9669)
    ],
    State.BB: [
        zip_code_range(1941, 1998),
        zip_code_range(3001, 3253),
        zip_code_range(4891, 4938),
        zip_code_range(14401, 14715),
        zip_code_range(14723, 16949),
        zip_code_range(17258, 17258),
        zip_code_range(17261, 17291),
        zip_code_range(17309, 17309),
        zip_code_range(17321, 17321),
        zip_code_range(17326, 17326),
        zip_code_range(17335, 17335),
        zip_code_range(17337, 17337),
        zip_code_range(19307, 19357)
    ],
    State.TH: [
        zip_code_range(4581, 4639),
        zip_code_range(6551, 6578),
        zip_code_range(7301, 7919),
        zip_code_range(7919, 7919),
        zip_code_range(7920, 7950),
        zip_code_range(7952, 7952),
        zip_code_range(7953, 7980),
        zip_code_range(7985, 7985),
        zip_code_range(7985, 7989),
        zip_code_range(36401, 36469),
        zip_code_range(37301, 37359),
        zip_code_range(96501, 96529),
        zip_code_range(98501, 99998)
    ],
    State.ST: [
        zip_code_range(6001, 6548),
        zip_code_range(6601, 6928),
        zip_code_range(14715, 14715),
        zip_code_range(29401, 29416),
        zip_code_range(38481, 38489),
        zip_code_range(38801, 39649)
    ],
    State.BE: [
        zip_code_range(10001, 14330)
    ],
    State.MV: [
        zip_code_range(17001, 17256),
        zip_code_range(17258, 17259),
        zip_code_range(17301, 17309),
        zip_code_range(17309, 17321),
        zip_code_range(17321, 17322),
        zip_code_range(17328, 17331),
        zip_code_range(17335, 17335),
        zip_code_range(17337, 19260),
        zip_code_range(19273, 19273),
        zip_code_range(19273, 19306),
        zip_code_range(19357, 19417),
        zip_code_range(23921, 23999)
    ],
    State.NI: [
        zip_code_range(19271, 19273),
        zip_code_range(21202, 21449),
        zip_code_range(21522, 21522),
        zip_code_range(21601, 21789),
        zip_code_range(26001, 27478),
        zip_code_range(27607, 27809),
        zip_code_range(28784, 29399),
        zip_code_range(29431, 31868),
        zip_code_range(34331, 34353),
        zip_code_range(34355, 34355),
        zip_code_range(37001, 37194),
        zip_code_range(37197, 37199),
        zip_code_range(37401, 37649),
        zip_code_range(37689, 37691),
        zip_code_range(37697, 38479),
        zip_code_range(38501, 38729),
        zip_code_range(48442, 48465),
        zip_code_range(48478, 48480),
        zip_code_range(48486, 48488),
        zip_code_range(48497, 48531),
        zip_code_range(49001, 49459),
        zip_code_range(49551, 49849)
    ],
    State.HH: [
        zip_code_range(20001, 21037),
        zip_code_range(21039, 21170),
        zip_code_range(22001, 22113),
        zip_code_range(22115, 22143),
        zip_code_range(22145, 22145),
        zip_code_range(22147, 22786),
        zip_code_range(27499, 27499)
    ],
    State.SH: [
        zip_code_range(21039, 21039),
        zip_code_range(21451, 21521),
        zip_code_range(21524, 21529),
        zip_code_range(22113, 22113),
        zip_code_range(22145, 22145),
        zip_code_range(22145, 22145),
        zip_code_range(22801, 23919),
        zip_code_range(24001, 25999),
        zip_code_range(27483, 27498)
    ],
    State.HB: [
        zip_code_range(27501, 27580),
        zip_code_range(28001, 28779)
    ],
    State.NW: [
        zip_code_range(32001, 33829),
        zip_code_range(34401, 34439),
        zip_code_range(37651, 37688),
        zip_code_range(37692, 37696),
        zip_code_range(40001, 48432),
        zip_code_range(48466, 48477),
        zip_code_range(48481, 48485),
        zip_code_range(48489, 48496),
        zip_code_range(48541, 48739),
        zip_code_range(49461, 49549),
        zip_code_range(50101, 51597),
        zip_code_range(51601, 53359),
        zip_code_range(53581, 53604),
        zip_code_range(53621, 53949),
        zip_code_range(57001, 57489),
        zip_code_range(58001, 59966),
        zip_code_range(59969, 59969)
    ],
    State.HE: [
        zip_code_range(34001, 34329),
        zip_code_range(34355, 34355),
        zip_code_range(34356, 34399),
        zip_code_range(34441, 36399),
        zip_code_range(37194, 37195),
        zip_code_range(37201, 37299),
        zip_code_range(55240, 55252),
        zip_code_range(59969, 59969),
        zip_code_range(60001, 63699),
        zip_code_range(63776, 63776),
        zip_code_range(64201, 64753),
        zip_code_range(64754, 65326),
        zip_code_range(65327, 65391),
        zip_code_range(65392, 65556),
        zip_code_range(65583, 65620),
        zip_code_range(65627, 65627),
        zip_code_range(65701, 65936),
        zip_code_range(68501, 68519),
        zip_code_range(68601, 68649),
        zip_code_range(69235, 69239),
        zip_code_range(69430, 69431),
        zip_code_range(69434, 69434),
        zip_code_range(69479, 69488),
        zip_code_range(69503, 69509),
        zip_code_range(69515, 69518)
    ],
    State.RP: [
        zip_code_range(51598, 51598),
        zip_code_range(53401, 53579),
        zip_code_range(53614, 53619),
        zip_code_range(54181, 55239),
        zip_code_range(55253, 56869),
        zip_code_range(57501, 57648),
        zip_code_range(65326, 65326),
        zip_code_range(65391, 65391),
        zip_code_range(65558, 65582),
        zip_code_range(65621, 65626),
        zip_code_range(65629, 65629),
        zip_code_range(66461, 66509),
        zip_code_range(66841, 67829),
        zip_code_range(76711, 76891)
    ],
    State.BY: [
        zip_code_range(63701, 63774),
        zip_code_range(63776, 63928),
        zip_code_range(63930, 63939),
        zip_code_range(74594, 74594),
        zip_code_range(80001, 87490),
        zip_code_range(87493, 87561),
        zip_code_range(87571, 87789),
        zip_code_range(88101, 88146),
        zip_code_range(88147, 88179),
        zip_code_range(89081, 89081),
        zip_code_range(89087, 89087),
        zip_code_range(89201, 89449),
        zip_code_range(90001, 96489),
        zip_code_range(97001, 97859),
        zip_code_range(97888, 97892),
        zip_code_range(97896, 97896),
        zip_code_range(97901, 97909)
    ],
    State.BW: [
        zip_code_range(63928, 63928),
        zip_code_range(64754, 64754),
        zip_code_range(68001, 68312),
        zip_code_range(68520, 68549),
        zip_code_range(68701, 69234),
        zip_code_range(69240, 69429),
        zip_code_range(69434, 69434),
        zip_code_range(69435, 69469),
        zip_code_range(69489, 69502),
        zip_code_range(69510, 69514),
        zip_code_range(70001, 74592),
        zip_code_range(74594, 76709),
        zip_code_range(77601, 79879),
        zip_code_range(88001, 88099),
        zip_code_range(88147, 88147),
        zip_code_range(88181, 89079),
        zip_code_range(89081, 89085),
        zip_code_range(89090, 89198),
        zip_code_range(89501, 89619),
        zip_code_range(97861, 97877),
        zip_code_range(97893, 97896),
        zip_code_range(97897, 97900),
        zip_code_range(97911, 97999)
    ],
    State.SL: [
        zip_code_range(66001, 66459),
        zip_code_range(66511, 66839)
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
