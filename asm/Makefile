AS := /opt/devkitpro/devkitPPC/bin/powerpc-eabi-as
LD := /opt/devkitpro/devkitPPC/bin/powerpc-eabi-ld
ASFLAGS := -mgekko
LDFLAGS := --oformat=binary

all: relloader.bin jmp.bin filename.bin

relloader.o:
	$(AS) $(ASFLAGS) -o relloader.o relloader.asm

jmp.o:
	$(AS) $(ASFLAGS) -o jmp.o jmp.asm

filename.o:
	$(AS) $(ASFLAGS) -o filename.o filename.asm

relloader.bin: relloader.o
	$(LD) $(LDFLAGS) -o relloader.bin relloader.o

jmp.bin: jmp.o
	$(LD) $(LDFLAGS) -o jmp.bin jmp.o

filename.bin: filename.o
	$(LD) $(LDFLAGS) -o filename.bin filename.o

clean:
	rm *.o *.bin
