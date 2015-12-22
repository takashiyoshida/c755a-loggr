#ifndef GLOBAL_H
#define GLOBAL_H

#include "Global_header.h"

struct CompareIt;

#include "EvarData.h"
#include "ExcData.h"

//////////////////////////////////////
// define statement
//////////////////////////////////////
/* ID of SWC */
#define kRTU_ID 0x00
#define kSIGNALLING_ID 0x10
#define kPOWER_ID 0x20
#define kPOWER2_ID 0x21		/*	Only used in Depot */
#define kPOWER3_ID 0x22		/*	Only used in Depot */
#define kPIS_ID 0x30
#define kCCTV_ID 0x40
#define kCLOCK_ID 0x50
#define kPAS_ID 0x60
#define kLIFT1_ID 0x70
#define kLIFT2_ID 0x71
#define kLIFT3_ID 0x72
#define kLIFT4_ID 0x73
#define kLIFT5_ID 0x74
#define kLIFT6_ID 0x75
#define kESC_ID 0x80
#define kECS_ID 0x90
#define kFIRE_ID 0xA0
#define kWASH_ID 0xB0
#define kPLC1_ID 0xF0
#define kPLC2_ID 0xF1
#define kPLC3_ID 0xF2
#define kPLC4_ID 0xF3
#define kPLC5_ID 0xF4

#define kMIN_LENGTH 8 /* minimal length of a message */
#define kREAD_N_WORDS 0x04
#define kREAD_REGISTERS 0x03
#define kWRITE_N_WORDS 0x10
#define kREAD_N_BITS 0x02
#define kWRITE_N_BITS 0x0F
#define kSLAVE_NUM_RS 0x05 /* slave number when PMS is writing towards */
                           /* servers (slave adress of server) RTU -> Server */
#define kSLAVE_NUM_SR 0x00 /* slave number when server writes towards PMS */
                           /* (servers are masters) Server -> RTU */


//////////////////////////////////////
// Global Declaration
//////////////////////////////////////
extern string SpyLogFileName;
extern string ExcFileName;
extern string EvarFileName;
extern string EquName;

extern char szMsgHdr[256];
extern unsigned int auiData[2048];
extern unsigned int uiCount;
extern unsigned int uiCurrentCount;
extern unsigned int uiDataLength;


extern EvarDataMgr EvarDataSet;
extern ExcDataMgr ExcDataSet;

//////////////////////////////////////
// Global Function Declaration
//////////////////////////////////////
void StoreFileName(int argc, char *argv[]);
void Displaydata();
void ProcessDO(string strSystemId, string strTableId);
void PrintUsage(char **);

#endif // GLOBAL_H
