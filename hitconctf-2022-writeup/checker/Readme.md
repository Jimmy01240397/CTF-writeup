# checker

![image](https://user-images.githubusercontent.com/57281249/204158150-d012979f-8227-450d-a458-be0d2ffa67f9.png)

Disassemble checker.exe and checker_drv.sys using IDA Pro. We can know that the checker sends the 0x222080u code to the checker_drv driver to check if there is a "hitcon" at address 0x140003000.

checker.exe: 

![image](https://user-images.githubusercontent.com/57281249/204158308-726e9f4c-04f3-48de-b588-0a1f603af5a0.png)

checker_drv.sys: 

![image](https://user-images.githubusercontent.com/57281249/204158381-0616e107-20b6-4e4c-9fa7-6c7e6e5cf9fc.png)

Also, there are other codes that can be sent that will use the data from addresses 0x140003030 to 0x14000312F to change the function at address 0x14001B30, and then use that function to calculate the hex data from addresses 0x140003000 to 0x14000302A.

checker_drv.sys: 

![image](https://user-images.githubusercontent.com/57281249/204158683-35f275c5-6d17-46f9-9082-908e0bfef896.png)
![image](https://user-images.githubusercontent.com/57281249/204158704-5374f7af-1d8c-4dd9-9c76-1aa5ef62d02c.png)

When the driver is loaded, it will first use the data from address 0x140001430 to 0x14000144A to change the hexadecimal data at address 0x14001B30.

checker_drv.sys: 

![image](https://user-images.githubusercontent.com/57281249/204158746-cdac8ff7-2d75-4ba7-8dcf-363da013e6b3.png)

We need to send these codes in a specific order to get the correct flags.

We can find the order by choosing the code that makes the disassembly of function 0x14001B30 valid.

The order is 0x222070u,0x222020u,0x222060u,0x222000u,0x222010u,0x222040u,0x222030u,0x222050u

Then use the function we got to calculate the hex for addresses 0x140003000 to 0x14000302A and then we can get the flags.

## Exploit
### exploit1
Use exploit1 to choose the order of codes.
``` python
import sys

sourcedata3180 = bytes.fromhex('80E92280F1AD0FB6C16BC811B89E0000')

data3188 = bytes.fromhex('40534883EC20488B053B0C0000488BDA488B4A104839087537488B4A08FF151D')

data3178 = bytes.fromhex('19BC8F82D02C6134C09FF650D5FB0C6ED0EBE5E3CEB54CCA45AA11B23E626F7DD0EBA9E3B22F06477C28C5DEDE1A4ED6D82D934F826564FD08624B877E524730B7BAD039685350AB20D5CA8426716F911B364611A5F14E586C74D49C15E228D5D90F3D83F3FCD1131A621240AAEACDCBE1C6088198F66888BE23B59E55B9E27D5ADA3907F02E322059564CB48F3E0761D90F2D61F1913314CB4968FE1FD48AFEE1C618639A9B8A8A7F08C3E8E1EC0B8F3B0094A511E74766C49F981870F030F69471B195D1F06FB7D93D059EC15333769B4B69CADEFD7D67B8292BC7C5842CD18787F1989774AD4B32F04A5172EA09F738FD27BD1C527143959C1A86F2C0F9F8')

data3180 = bytearray(sourcedata3180)

for a in range(32):
    data3180[a%16] = data3180[a%16] ^ data3188[a]

sourcedata3180 = bytes(data3180)

print(f"usage: {sys.argv[0]} <index 0(0~7)> <index 1>  <index 2> ...")

order=[ int(a) for a in sys.argv[1:len(sys.argv)] ]

codes=list(range(8))

for i in range(8):
    print("index " + str(i) + ": ")
    if i >= len(order):
        for now in range(8):
            data3180 = bytearray(sourcedata3180)
            for a in range(0,16):
                data3180[a] = data3180[a] ^ data3178[now*0x20 + a]
            print("try " + str(now) + ": " + bytes(data3180).hex())
        x = int(input("select code (0~7): "))
        while x < 0 and x > 7:
            x=int(input("select code (0~7): "))
        order.append(x)
    data3180 = bytearray(sourcedata3180)
    for a in range(0,16):
        data3180[a] = data3180[a] ^ data3178[order[i]*0x20 + a]
    print(str(order[i]) + ": " + bytes(data3180).hex())
    for a in range(0,16):
        data3180[a] = data3180[a] ^ data3178[order[i]*0x20 + 0x10 + a]
    sourcedata3180 = bytes(data3180)
```

### exploit2
Use exploit2 for get flag.
``` C
#include<stdio.h>
#include<string.h>

#define _BYTE unsigned char
#define __int64 long long
#define __int8 char

typedef __int64 (*func)(int);

__int64 func0(unsigned __int8 a1)
{
  __int64 result; // rax

  result = (8 * a1) | (a1 >> 5);
  return result;
}

__int64 func1(unsigned __int8 a1)
{
  return a1 ^ 0x26u;
}

__int64 func2(unsigned __int8 a1)
{
  __int64 result; // rax

  result = (16 * a1) | (a1 >> 4);
  return result;
}

__int64 func3(int a1)
{
  return (unsigned int)(a1 + 55);
}

__int64 func4(int a1)
{
  return (unsigned int)(a1 + 123);
}

__int64 func5(unsigned __int8 a1)
{
  __int64 result; // rax

  result = (a1 << 7) | (a1 >> 1);
  return result;
}

__int64 func6(unsigned __int8 a1)
{
  return 173 * (unsigned int)a1;
}

__int64 func7(unsigned __int8 a1)
{
  __int64 result; // rax

  result = (4 * a1) | (a1 >> 6);
  return result;
}

int main()
{
    char *defaultdatahex = "6360A5B9FFFC300A48BBFEFE322C0AD6E6FEFE322C0AD6BB4A4A322CFCFF0AFDBBFE2CB963D6B962D60A4F";
    char datahex[1000] = {0}, data[50] = {0};

    if(defaultdatahex) strcpy(datahex, defaultdatahex);
    else gets(datahex);
    for(int i = 0, count = 0; datahex[i]; count++)
    {
        char now[3] = {0};
        for(int k = 0; k < 2; k++, i++)
        {
            if((datahex[i] >= 'A' && datahex[i] <= 'F') || (datahex[i] >= 'a' && datahex[i] <= 'f') || (datahex[i] >= '0' && datahex[i] <= '9'))
            {
                now[k] = datahex[i];
            }
            else
            {
                k--;
            }
        }
        sscanf(now, "%x", &data[count]);
    }

    func allfunc[8] = {func0,func1,func2,func3,func4,func5,func6,func7};

    for(int i = 0; i < 8; i++)
    {
        for(int k = 0; k < 43; k++)
        {
            data[k] = allfunc[i](data[k]);
        }
    }

    printf("hex: ");
    for(int i = 0; i < 43; i++)
    {
        printf("%02x ", (unsigned char)data[i]);
    }
    printf("\n");
    printf("%s\n", data);
}
```

## Flag
`hitcon{r3ally_re4lly_rea11y_normal_checker}`
