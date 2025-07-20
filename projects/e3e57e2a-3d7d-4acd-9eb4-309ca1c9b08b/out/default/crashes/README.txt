Command line used to find this crash:

afl-fuzz -i /home/parrot/Desktop/fyp/projects/e3e57e2a-3d7d-4acd-9eb4-309ca1c9b08b/in -o /home/parrot/Desktop/fyp/projects/e3e57e2a-3d7d-4acd-9eb4-309ca1c9b08b/out -V 100 -m none -- /home/parrot/Desktop/fyp/projects/e3e57e2a-3d7d-4acd-9eb4-309ca1c9b08b/code.cpp_binary @@

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please post
to https://github.com/AFLplusplus/AFLplusplus/issues/286 once the issues
 are fixed :)

