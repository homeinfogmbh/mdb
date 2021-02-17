/*
    mdb.mjs - Library for MDB data structures.

    (C) 2020-2021 HOMEINFO - Digitale Informationssysteme GmbH

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
    Represents an address.
*/
export class Address {
    constructor (street, houseNumber, zipCode, city) {
        this.street = street;
        this.houseNumber = houseNumber;
        this.zipCode = zipCode;
        this.city = city;
    }

    static fromJSON (json) {
        return new this(json.street, json.houseNumber, json.zipCode, json.city);
    }

    get streetHouseNumber () {
        return [this.street, this.houseNumber].join(' ');
    }

    get zipCodeCity () {
        return [this.zipCode, this.city].join(' ');
    }

    toString () {
        return [this.streetHouseNumber, this.zipCodeCity].join(', ');
    }
}


/*
    Represents a company.
*/
export class Company {
    constructor (id, name, abbreviation, address) {
        this.id = id;
        this.name = name;
        this.abbreviation = abbreviation;
        this.address = address;
    }

    static fromJSON (json) {
        return new this(json.id, json.name, json.abbreviation, address);
    }
}


/*
    Represents a customer.
*/
export class Customer {
    constructor (id, company) {
        this.id = id
        this.company;
    }

    static fromJSON (json) {
        const company = Company.fromJSON(json.company);
        return new this(json.id, company);
    }

    get name () {
        return this.company.name;
    }

    get abbreviation () {
        return this.company.abbreviation;
    }

    get address () {
        return this.company.address;
    }

    toString (preferAbbreviation = false, withId = true) {
        let result;

        if (preferAbbreviation)
            result = this.abbreviation || this.name;
        else
            result = this.name;

        if (withId)
            return result + ' (' + this.id + ')';

        return result;
    }
}


/*
    Converts a JSON object representing an address into a one-line string.
*/
export function addressToString (address) {
    return Address.fromJSON(address).toString();
}


/*
    Converts a JSON object representing a customer into a one-line string.
*/
export function customerToString (customer, preferAbbreviation = false, withId = true) {
    return Customer.fromJSON(customer).toString(preferAbbreviation, withId);
}
