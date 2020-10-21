/*
    mdb.js - Library for MDB data structures.

    (C) 2020 HOMEINFO - Digitale Informationssysteme GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Maintainer: Richard Neumann <r dot neumann at homeinfo period de>
*/
'use strict';

/*
    Returns the respective address as a one-line string.
*/
export function addressToString (address, sep = ', ', shSep = ' ', zcSep = ' ') {
    const streetHouseno = [address.street, address.houseNumber];
    const zipCodeCity = [address.zipCode, address.city];
    const addressElements = [streetHouseno.join(shSep), zipCodeCity.join(zcSep)];
    return  addressElements.join(sep);
}


/*
    Returns the respective customer as a one-line string.
*/
export function customerToString (customer, preferAbbreviation = false, withId = true, idPrefix = '(', idSuffix = ')') {
    const elements = [];

    if (preferAbbreviation)
        elements.push(customer.company.abbreviation || customer.company.name);
    else
        elements.push(customer.company.name);

    if (withId)
        const customerId = [idPrefix || '', customer.id, idSuffix || ''];
        elements.push(customerId.join(''));

    return elements.join(' ');
}
