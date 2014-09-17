'''
I FUCKING HATE JAVASCRIPT

Copyright (c) 2014 Tom Stroobants <stroobantstom@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.


function base64encode(str) {
    var out, i, len;
    var c1, c2, c3;
    len = str.length;
    i = 0;
    out = '';
    while (i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == len) {
            out += g_base64EncodeChars.charAt(c1 >> 2);
            out += g_base64EncodeChars.charAt((c1 & 0x3) << 4);
            out += '==';
            break;
        }
        c2 = str.charCodeAt(i++);
        if (i == len) {
            out += g_base64EncodeChars.charAt(c1 >> 2);
            out += g_base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += g_base64EncodeChars.charAt((c2 & 0xF) << 2);
            out += '=';
            break;
        }
        c3 = str.charCodeAt(i++);
        out += g_base64EncodeChars.charAt(c1 >> 2);
        out += g_base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        out += g_base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        out += g_base64EncodeChars.charAt(c3 & 0x3F);
    }
    return out;
}

This is the javascript that was needed to be converted. First let us look up the functions.

out, i, len, c1, c2, c3 are all variabeles without any value

len is the str length so len() in python
i is initialized on zero
out is initialized on empty string

while loop that will continue as long i is under length

Javascript & Python bitwise operators are the same so copy paste!
CharCodeAt is ord()
charAt is str[index]
break is break
'''


def js_base64(inp_str):
	base64_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	length = len(inp_str)
	i = 0
	out = ""
	while i < length:
		c1 = ord(inp_str[i]) & 0xff
		i += 1 #Python doesn't have ++
		if i == length:
			out += base64_str[c1 >> 2]
			out += base64_str[(c1 & 0x3) << 4]
			out += "=="
			break

		c2 = ord(inp_str[i])
		i += 1
		if i == length:
			out += base64_str[c1 >> 2]
			out += base64_str[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
			out += base64_str[(c2 & 0xF) << 2]
			out += '='
			break

		c3 = ord(inp_str[i])
		i += 1
		out += base64_str[c1 >> 2]
		out += base64_str[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
		out += base64_str[((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6)]
		out += base64_str[c3 & 0x3F]
	return out

print js_base64("admin")
