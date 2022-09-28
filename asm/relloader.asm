# This is a patched version of:
# https://github.com/TheBombSquad/ApeSphere-Custom/blob/master/relloader/iso-rel-loader-us.ApeSphere-Custom
# Made to work with gnu-as, as included with devkitppc, so it can be injected
# without heavy dependencies.

# Define the registers.
    .set r0, 0
    .set r1, 1
    .set r2, 2
    .set r3, 3
    .set r4, 4
    .set r5, 5
    .set r6, 6
    .set r7, 7
    .set r8, 8
    .set r9, 9
    .set r10, 10
    .set r11, 11
    .set r12, 12
    .set r13, 13
    .set r14, 14
    .set r15, 15
    .set r16, 16
    .set r17, 17
    .set r18, 18
    .set r19, 19
    .set r20, 20
    .set r21, 21
    .set r22, 22
    .set r23, 23
    .set r24, 24
    .set r25, 25
    .set r26, 26
    .set r27, 27
    .set r28, 28
    .set r29, 29
    .set r30, 30
    .set r31, 31

._start:
    lwz r3, 0(r31)          # Pointer to the Main Loop's Module
    lwz r3, 0(r3)           # Pointer to the Main Loop's Module Id
    cmpwi r3, 0x1
    bne .exit

    # Initialize static values used for addresses
    # Do not overwrite r31
    lis r30, 0x8002
    lis r29, 0x8001
    lis r28, 0x8000

    li r27, 0               # Used to check if a REL file is loaded or not

    # Back up the current Arena Low
    lwz r25, -0x7f50(r13)   # Arena Low

    # Allocate memory for the CARDMount work area, CardFileInfo, 
    # and the initial 0x200 bytes for reading from the memory card
    ori r3, r27, 0xa220
    bl .allocateFromArenaLow

    # Backup the returned address to be used for later
    mr r26, r3

    # Open file on DVD
    ori r3, r29, 0x87a0     # DVDOpen
    .long 0x7c6903a6        # mtctr r3
    lis r3, 0x800a
    ori r3, r3, 0x9a5c      # File name pointer (argument 1)
    mr r4, r26              # File info pointer (argument 2)
    .long 0x4e800421        # bctrl
    cmpwi r3, 0
    beq .exit

    # Get filesize
    lwz r24, 0x34(r26)
    addi r24, r24, 31       # add 31 to round down for 32-byte alignment
    rlwinm r24, r24, 0, 0, 26  # 32-byte alignment w/ mask 0xffffffe0
    mr r3, r24      

    # Allocate memory for the file
    lwz r23, 0(r31)         # ptr to main loop module
    lwz r23, 0x24(r23)      # ptr to relocation data
    addi r23, r23, 31       
    rlwinm r23, r23, 0, 0, 26 # round to nearest 0x20
    mr r3, r24              # file size
    bl .allocateFromMainLoopRelocMemory
    mr r22, r3              # move returned address to r22

    # Read file from DVD
    ori r3, r28, 0x92fc     # read_entire_file_using_dvdread_prio_async
    .long 0x7c6903a6        # mtctr r3
    mr r3, r26              # File info pointer (argument 1)
    mr r4, r22              # File buffer (argument 2)
    mr r5, r24              # File size (argument 3)
    li r6, 0x0              # File offset (argument 4)
    .long 0x4e800421        # bctrl r3

    # Allocate memory for BSS area
    lwz r3, 0x20(r22)       # get BSS area size
    bl .allocateFromMainLoopRelocMemory
    mr r21, r3              # save BSS ptr in r21

    # OSLink
    ori r3, r29, 0x730      # OSLInk
    .long 0x7c6903a6        # mtctr r3
    mr r3, r22              # module ptr
    mr r4, r21              # BSS area
    .long 0x4e800421        # bctrl
    cmpwi r3, 0x1           # check for errors
    bne .callOSUnlink

    lwz r3, 0(r31)          # ptr to main loop's module
    stw r3, 0x4524(r28)
    lwz r3, 0x4(r31)        # ptr to main loop's BSS area
    stw r3, 0x4528(r28)   
    stw r23, 0x452c(r28)    # ptr to main loop's relocation data
    stw r21, 0x4530(r28)    # ptr to BSS area
    stw r22, 0x4532(r28)    # ptr to module

    lwz r27, 0x34(r22)      # prolog ptr

    b .DVDClose

.callOSUnlink:
    ori r3, r29, 0xb8c      # OSUnlink
    .long 0x7c6903a6        # mtctr r3
    mr r3, r22              # ptr to module
    .long 0x4e800421        # bctrl

.DVDClose:
    ori r3, r29, 0x8868     # DVDClose
    .long 0x7c6903a6        # mtctr r3
    mr r3, r26              # file info ptr
    .long 0x4e800421        # bctrl

# Run REL prolog
.freeMemory:
    stw r25, -0x7f50(r13)   # restore arena low
    cmpwi r27, 0
    beq .exit
    .long 0x7f6903a6        # mtctr r27
    .long 0x4e800421        # bctrl
    b .exit

.allocateFromArenaLow:
    stwu r1, -0x10(r1)
    mflr r0
    stw r0, 0x14(r1)
    .long 0xbfc10008        # stmw r30,0x8(r1)
    ori r4, r28, 0xd5a8     # OSAllocFromArenaLow
    .long 0x7c8903a6        # mtctr r4
    addi r3, r3, 31
    rlwinm r3, r3, 0, 0, 26 # Round the size up to the nearest multiple of 0x20
                            # bytes
    mr r31, r3              # Size
    li r4, 32               # Alignment
    .long 0x4e800421        # bctrl
    b .clearAndFlushMemory

.allocateFromMainLoopRelocMemory:
    stwu r1, -0x10(r1)
    mflr r0
    stw r0, 0x14(r1)
    .long 0xbfc10008        # stmw r30, 0x8(r1)

    addi r4, r3, 31
    rlwinm r4, r4, 0, 0, 26 # round to nearest multiple of 0x20
    mr r31, r4              # size/amount to allocate
    mr r3, r23  

    add r23,r23, r4         # next spot in main loop's relocation data

.clearAndFlushMemory:
    ori r5, r28, 0x33a8     # memset
    .long 0x7ca903a6        # mtctr r5
    mr r30, r3              # Dest
    li r4, 0
    mr r5, r31              # Size
    .long 0x4e800421        # bctrl

    # Flush the memory
    ori r3, r28, 0xd8cc     # DCFlushRange
    .long 0x7c6903a6        # mtctr r3
    mr r3, r30              # Dest
    mr r4, r31              # Size
    .long 0x4e800421        # bctrl
    mr r3, r30              # Dest

    .long 0xbbc10008        # lmw r30,0x8(r1)
    lwz r0, 0x14(r1)
    mtlr r0
    addi r1, r1, 0x10
    blr

.exit:
    lwz r3, 0(r31)          # Pointer to the Main Loop's Moduleo 
                            # (replaces overwritten instruction)
    ori r9, r28, 0x6d0c     # this is done because the call stack doesn't
                            #behave like a stack for some reason? 
    .long 0x7d2803a6        # mtspr LR, r9
    blr
