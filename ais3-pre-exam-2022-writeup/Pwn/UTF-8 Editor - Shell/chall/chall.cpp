#include <stdint.h>
#include <stdlib.h>
#include <iostream>
#include <vector>

// you don't need to find vulnerability in the copied code

// copied from https://github.com/skeeto/branchless-utf8/blob/master/utf8.h
static void *utf8_decode(const void *buf, uint32_t *c, int *e) {
	static const char lengths[] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	                               1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
	                               0, 0, 2, 2, 2, 2, 3, 3, 4, 0};
	static const int masks[] = {0x00, 0x7f, 0x1f, 0x0f, 0x07};
	static const uint32_t mins[] = {4194304, 0, 128, 2048, 65536};
	static const int shiftc[] = {0, 18, 12, 6, 0};
	static const int shifte[] = {0, 6, 4, 2, 0};

	unsigned char *s = (unsigned char *)buf;
	int len = lengths[s[0] >> 3];

	/* Compute the pointer to the next character early so that the next
     * iteration can start working on the next character. Neither Clang
     * nor GCC figure out this reordering on their own.
     */
	unsigned char *next = s + len + !len;

	/* Assume a four-byte character and load four bytes. Unused bits are
     * shifted out.
     */
	*c = (uint32_t)(s[0] & masks[len]) << 18;
	*c |= (uint32_t)(s[1] & 0x3f) << 12;
	*c |= (uint32_t)(s[2] & 0x3f) << 6;
	*c |= (uint32_t)(s[3] & 0x3f) << 0;
	*c >>= shiftc[len];

	/* Accumulate the various error conditions. */
	*e = (*c < mins[len]) << 6;       // non-canonical encoding
	*e |= ((*c >> 11) == 0x1b) << 7;  // surrogate half?
	*e |= (*c > 0x10FFFF) << 8;       // out of range?
	*e |= (s[1] & 0xc0) >> 2;
	*e |= (s[2] & 0xc0) >> 4;
	*e |= (s[3]) >> 6;
	*e ^= 0x2a;  // top two bits of each tail byte correct?
	*e >>= shifte[len];

	return next;
}
// copied from https://gist.github.com/MightyPork/52eda3e5677b4b03524e40c9f0ab1da5
int utf8_encode(char *out, uint32_t utf) {
	if (utf <= 0x7F) {
		// Plain ASCII
		out[0] = (char)utf;
		out[1] = 0;
		return 1;
	} else if (utf <= 0x07FF) {
		// 2-byte unicode
		out[0] = (char)(((utf >> 6) & 0x1F) | 0xC0);
		out[1] = (char)(((utf >> 0) & 0x3F) | 0x80);
		out[2] = 0;
		return 2;
	} else if (utf <= 0xFFFF) {
		// 3-byte unicode
		out[0] = (char)(((utf >> 12) & 0x0F) | 0xE0);
		out[1] = (char)(((utf >> 6) & 0x3F) | 0x80);
		out[2] = (char)(((utf >> 0) & 0x3F) | 0x80);
		out[3] = 0;
		return 3;
	} else if (utf <= 0x10FFFF) {
		// 4-byte unicode
		out[0] = (char)(((utf >> 18) & 0x07) | 0xF0);
		out[1] = (char)(((utf >> 12) & 0x3F) | 0x80);
		out[2] = (char)(((utf >> 6) & 0x3F) | 0x80);
		out[3] = (char)(((utf >> 0) & 0x3F) | 0x80);
		out[4] = 0;
		return 4;
	} else {
		// error - use replacement character
		out[0] = (char)0xEF;
		out[1] = (char)0xBF;
		out[2] = (char)0xBD;
		out[3] = 0;
		return 0;
	}
}

class utf8_string {
   public:
	std::vector<uint32_t> data;  // UTF-8 codepoints
	friend std::istream &operator>>(std::istream &is, utf8_string &obj);
	friend std::ostream &operator<<(std::ostream &os, utf8_string &obj);

   public:
	size_t length() { return data.size() - 1; }
	uint32_t &operator[](int i) { return data[i]; }
};

std::istream &operator>>(std::istream &is, utf8_string &obj) {
	std::string s;
	is >> s;
	const char *sptr = s.c_str();
	while (*sptr != 0) {
		int err = 0;
		uint32_t tmp;
		sptr = (const char *)utf8_decode(sptr, &tmp, &err);
		if (err) {
			return is;
		}
		obj.data.push_back(tmp);
	}
	obj.data.push_back(0);  // null terminated
	return is;
}
std::ostream &operator<<(std::ostream &os, utf8_string &obj) {
	for (int i = 0; i < obj.length(); i++) {
		char buf[5];
		utf8_encode(buf, obj.data[i]);
		os << buf;
	}
	return os;
}

int main() {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	utf8_string str;
	std::cout << "Please enter your UTF-8 string: ";
	std::cin >> str;
	while (true) {
		std::cout << "======== Menu ========" << std::endl;
		std::cout << "1. Print the string" << std::endl;
		std::cout << "2. Edit a codepoint" << std::endl;
		std::cout << "3. Show a codepoint" << std::endl;
		std::cout << "4. Exit" << std::endl;
		std::cout << "> ";
		int c;
		std::cin >> c;
		if (c == 1) {
			std::cout << str << std::endl;
		} else if (c == 2) {
			std::cout << "Enter index: ";
			int idx;
			std::cin >> idx;
			if (0 <= idx && idx < str.length()) {
				std::cout << "Enter codepoint: ";
				uint32_t c;
				std::cin >> c;
				str[idx] = c;
			} else {
				std::cout << "Bad index" << std::endl;
			}
		} else if (c == 3) {
			std::cout << "Enter index: ";
			int idx;
			std::cin >> idx;
			if (0 <= idx && idx < str.length()) {
				std::cout << str[idx] << std::endl;
			} else {
				std::cout << "Bad index" << std::endl;
			}
		} else if (c == 4) {
			std::cout << "Bye" << std::endl;
			break;
		}
	}
	return 0;
}
