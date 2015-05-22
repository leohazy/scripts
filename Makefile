

#=============== Select GPU architectures ===============
#GENCODE:=$(GENCODE) -gencode=arch=compute_52,code=\"sm_52,compute_52\"
GENCODE:=$(GENCODE) -gencode=arch=compute_13,code=\"sm_13,compute_13\"
#GENCODE:=$(GENCODE) -gencode=arch=compute_20,code=\"sm_20,compute_20\"
##GENCODE:=$(GENCODE) -gencode=arch=compute_30,code=\"sm_30,compute_30\"
#GENCODE:=$(GENCODE) -gencode=arch=compute_35,code=\"sm_35,compute_35\"


DIRTOOLKIT=/usr/local/cuda-6.0
CCFLAGS=-c -O3 -ffast-math -Wno-format-security
INCLUDE= -I./ -I$(DIRTOOLKIT)/include  -I/usr/include/mpich -I /usr/local/culasparse/include
LIBS =  -L$(DIRTOOLKIT)/lib64 -L/usr/include/lib -L /usr/local/culasparse/lib64 -lcudart -lmpich -lmpl -lpthread  -lrt -lcula_sparse -lcolamd -lcublas -lcusparse -liomp5
NCC=$(DIRTOOLKIT)/bin/nvcc
NCCFLAGS = -c $(GENCODE)  -O3 -use_fast_math  
CC=/usr/bin/mpicxx

#-include list
CPPSRC = $(wildcard *.cpp)
OBJ_CPU = $(CPPSRC:.cpp=.o)
#OBJ_CPU = $(patsubst %cpp,%o,$(CPPSRC))
OBJ_GPU = Link_List_GPU.o
OBJ = $(OBJ_CPU)  $(OBJ_GPU)

.PHONY: all clean

all:MPS 
	rm -rf *.o
	@echo "  --- Compiled fin ---"
	mkdir -p build
	-mv MPS build

MPS : $(OBJ)
	$(CC) $(OBJ) $(LIBS) -o $@

%.o: %.cpp
	$(CC) $(CCFLAGS) $(INCLUDE) $< 
Link_List_GPU.o: Link_List_GPU.cu
	$(NCC) $(NCCFLAGS) $(INCLUDE) $(LIBS)  Link_List_GPU.cu

MPIRUN := mpirun
PROG := ./run
NP := 1


clean : 
	-rm *.o

