"""
Utility methods and classes
"""
from mimetypes import guess_extension
import magic
import sys

__date__ = '13.08.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['MIMEUtil', 'PDFUtil']


class MIMEUtil():
    """
    Common utility class
    """
    MIME_SUFFIX = {'image/jpeg': '.jpg',
                   'image/png': '.png',
                   'image/gif': '.gif',
                   'video/x-msvideo': '.avi',
                   'video/mpeg': '.mpg',
                   'video/quicktime': '.mov',
                   'video/x-flv': '.flv',
                   'application/pdf': '.pdf',
                   'application/xml': '.xml',
                   'text/html': '.html'}

    @classmethod
    def getmime(cls, file):
        """Read MIME type from file"""
        if type(file) is str:
            return magic.from_file(file, mime=True).decode()
        elif hasattr(file, 'read') and callable(getattr(file, 'read')):
            return magic.from_buffer(file.read(), mime=True).decode()
        else:
            return magic.from_buffer(file, mime=True).decode()

    @classmethod
    def getext(cls, file):
        """Read probably fitting extension from file"""
        mimetype = cls.getmime(file)
        extension = cls.MIME_SUFFIX.get(mimetype)
        return extension if extension else guess_extension(mimetype)


class PDFUtil():
    """
    Utility for PDF files
    """
    @classmethod
    def extrjpg(cls, f):
        """Extract JPEG files from a PDF document"""
        if type(f) == str:
            with open(sys.argv[1], "rb") as pdffile:
                pdf = pdffile.read()
        else:
            pdf = f
        result = []
        startmark = b"\xff\xd8"
        startfix = 0
        endmark = b"\xff\xd9"
        endfix = 2
        i = 0
        while True:
            istream = pdf.find("stream".encode(), i)
            if istream < 0:
                break
            istart = pdf.find(startmark, istream, istream+20)
            if istart < 0:
                i = istream+20
                continue
            iend = pdf.find("endstream".encode(), istart)
            if iend < 0:
                # Didn't find end of stream!
                return result
            iend = pdf.find(endmark, iend-20)
            if iend < 0:
                # Didn't find end of JPG!
                return result
            istart += startfix
            iend += endfix
            jpg = pdf[istart:iend]
            result.append(jpg)
            i = iend
        return result
