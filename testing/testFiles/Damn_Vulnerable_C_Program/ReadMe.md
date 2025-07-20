Note: file name has been changed from imgRead.c to dvcp.c, if you are watching videos, you will see imgRead.c but in github repo you will see dvcp.c, please use correct filename.

# Damn Vulnerable C Program(DVCP)             
[![Twitter Follow](https://img.shields.io/twitter/follow/hardik05?style=social)](https://twitter.com/hardik05)

**My YouTube Channel:** https://www.youtube.com/user/MrHardik05/featured?view_as=subscriber

**What it is?**

This is a simple C program which I have coded to explain common types of vulnerabilities like:
1. integer overflow
2. integer underflow
3. Out of bound Read
4. Out of bound Write
5. Double Free
6. Use After Free
7. Memory leaks
8. Stack exhaustion
9. Heap exhastion

This C program contains vulenrable code of all of the above vulnerabilities and you can fuzz it using any fuzzer like AFL, libafl, libfuzzer, hongfuzz, winafl, jackalope or any other fuzzer which you want. 

**How to Compile**

Just type "make" on the command prompt. Makefile is included with it.

**How to generate input for AFL?**

just create a sample input file as following and rest AFL will take care:

`echo "IMG" >input/1.txt`

AFL will automatically generate new test cases and discover most of the vulnerabilities mentioned above. thats the beauty of AFL :)

**How to fuzz it using AFL?**

**1. First compile this program using following command:**

`afl-gcc -g -fsanitize=address dvcp.c -o dvcp`

**2. run this command:** 

`afl-fuzz -i input -o output -m none -- ./dvcp @@`

**How to fuzz it using honggfuzz**

**1. First compile this program using following command:**

`hfuzz-gcc -g -fsanitize=address dvcp.c -o dvcp`

**2. run this command:** 

`hongfuzz -i input -- ./dvcp ___FILE___`

 **How to fuzz using libfuzzer**
 
You need to modify the C code, you can get the updated code from here: https://github.com/hardik05/Damn_Vulnerable_C_Program/blob/master/dvcp_libfuzzer.c

**1. Compile the program using following command:**

`clang -fsanitize=fuzzer,address,undefined -g dvcp_libfuzzer.c -o dvcp_libfuzzer`

**2. run this command to fuzz:**

`./dvcp_libfuzzer`


You can see the video tutorials here:

**Complete Fuzzing Playlist:**

https://www.youtube.com/watch?v=r7ucv2kN4j4&list=PLHGgqcJIME5kYhOSdJjvtVS4b4_OXDqM-

individual videos below:

**Linux**

**LibAFL**

**[Fuzzing with libAFL]How to install libAFL on system and what are the different components?** -> https://www.youtube.com/watch?v=ztGfxbvcrms

**[Fuzzing with libAFL]libAFL ForkSever Introduction, Running libAFL forkserver fuzzer.** -> https://www.youtube.com/watch?v=Ed1anYoGTyA

**[Fuzzing with libAFL]Fuzzing Damn Vulnerable C Program with libAFL forkserver fuzzer** -> https://www.youtube.com/watch?v=ad_4zroiS_g

**[Fuzzing with libAFL] Using shared memory mode with libAFL forkserver fuzzer** -> https://www.youtube.com/watch?v=GXD_qkISyfY


**AFL++**

**[Fuzzing with AFLplusplus] Installing AFLPlusplus and fuzzing a simple C program** -> https://www.youtube.com/watch?v=9wRVo0kYSlc

**[Fuzzing with AFLplusplus] How to fuzz a binary with no source code on Linux in persistent mode** -> https://www.youtube.com/watch?v=LGPJdEO02p4

**AFL**

**[Fuzzing with AFL] How to install AFL on Ubuntu**-> https://www.youtube.com/watch?v=r7ucv2kN4j4

**[Fuzzing with AFL] Fuzzing a simple C program with AFL** -> https://www.youtube.com/watch?v=NiGC1jxFx78&t=66s

**[Fuzzing with AFL] Finding different types of vulnerabilities with AFL** -> https://www.youtube.com/watch?v=m1RkShHzx_8&t=151s

**[Fuzzing with AFL] Triaging crashes with crashwalk and finding root cause with GDB** -> https://www.youtube.com/watch?v=5R2gPkCXZkM

**[Fuzzing with AFL] Fuzzing a binary with no source code with AFL in Qemu mode.**-> https://www.youtube.com/watch?v=np3sLLFQs6I

**Honggfuzz**

**[Fuzzing with honggfuzz] Fuzzing a simple C program with HongFuzz** -> https://www.youtube.com/watch?v=6OBXJtEe-d8

**[Fuzzing with honggfuzz] Hongfuzz,checksec(pwntools),ASAN** -> https://www.youtube.com/watch?v=Lr8pLQRTHac 

**Libfuzzer**

**[Fuzzing with libfuzzer] How to fuzz a simple C program using LibFuzzer** -> https://www.youtube.com/watch?v=hFva8kJQwnc&list=PLHGgqcJIME5m7HaHfACayoyN0TRe2PHRp

**[Fuzzing with libfuzzer,AFL] How to fuzz libfuzzer harness program using AFL** -> https://www.youtube.com/watch?v=HfEqm3TrfwM&list=PLHGgqcJIME5m7HaHfACayoyN0TRe2PHRp&index=2

**How to replicate OpenSSL vulnerabilities CVE-2022-3602 and CVE-2022-3786 and use libfuzzer** -> https://www.youtube.com/watch?v=vhTuXph1dtY

**Radamsa**

**[Fuzzing with Radamsa] Fuzzing a simple C program with Radamsa** -> https://youtu.be/1FRsXVNpynQ

**Windows**

**WinAFL**

**[Fuzzing with WinAFL] Fuzzing a simple C program with WinAFL** -> https://www.youtube.com/watch?v=Va_Wtxf3DMc

**[Fuzzing with WinAFL] What is a fuzzing function, how to make sure everything is working fine?** -> https://www.youtube.com/watch?v=HLORLsNnPzo

**I need more windows harness to fuzz with winafl**

sure, check here -> https://github.com/hardik05/winafl-harness

**i want to try something different may be some different mutators than winafl default ones..**

yep, you can try this -> https://github.com/hardik05/winafl-powermopt

more will be uploaded as i create them.

**OSS-Fuzz from google**

**How OSS-Fuzz Works: A Guide to Fuzz Testing for Open Source Projects** -> https://www.youtube.com/watch?v=OBxCDsJ-0aM

**Why you created this?**

It takes lot of time for new comers and even experianced people to understand different types of vulnerabilities. i have faced this problem myself and decided to share what i learned.

If you learn something from it, send me a thnak you note. thats all i need. Also if you want to improve of fix something then PR are welcomed!

**Author?**

**Twitter:** https://twitter.com/hardik05 

**Email:** DM me on twitter :)

**Web:** http://hardik05.wordpress.com

**Feedback?**

Suggestions and comments are always welcomed. if you find any issue or have a fix or a new feature send pull request.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hardik05/Damn_Vulnerable_C_Program&type=Date)](https://star-history.com/#hardik05/Damn_Vulnerable_C_Program&Date)


