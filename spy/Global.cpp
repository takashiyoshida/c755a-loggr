#include "Global_header.h"
#include "Global.h"

string SpyLogFileName;
string ExcFileName;
string EvarFileName;

string EquName = "";

char szMsgHdr[256] = "";
unsigned int auiData[2048];
unsigned int uiCount = 0;
unsigned int uiCurrentCount;
unsigned int uiDataLength;

enum TABLE_TYPE { DO, DO8, event, DI, DI8 };

EvarDataMgr EvarDataSet;
ExcDataMgr ExcDataSet;

//----------------------------------------
// RTU table types (SRS PMS section 4.4.2)
//----------------------------------------
const unsigned char DACCOMPMS_K_TABLE_EVENT = 0x00; // Event table
const unsigned char DACCOMPMS_K_TABLE_DI    = 0x01; // DI table
const unsigned char DACCOMPMS_K_TABLE_AI    = 0x02; // AI table
const unsigned char DACCOMPMS_K_TABLE_MI    = 0x03; // MI (metering input) table
const unsigned char DACCOMPMS_K_TABLE_DI8   = 0x04; // DI8 table
const unsigned char DACCOMPMS_K_TABLE_SI    = 0x05; // SI table
const unsigned char DACCOMPMS_K_TABLE_DO    = 0x06; // DO table
const unsigned char DACCOMPMS_K_TABLE_AO    = 0x07; // AO table
const unsigned char DACCOMPMS_K_TABLE_DO8   = 0x08; // DO8 table
const unsigned char DACCOMPMS_K_TABLE_SO    = 0x09; // SO table

//---------------------------
// RTU table format
//---------------------------
const unsigned short DACCOMPMS_K_SIZE_MODBUS_HEADER = 7;  // Modbus header size
const unsigned short DACCOMPMS_K_SIZE_TABLE_HEADER  = 18; // Table header size
const unsigned short DACCOMPMS_K_SIZE_HEADER = DACCOMPMS_K_SIZE_MODBUS_HEADER
                                             + DACCOMPMS_K_SIZE_TABLE_HEADER;
const unsigned short DACCOMPMS_K_SIZE_CRC = 2; // CRC size
const unsigned short DACCOMPMS_K_SIZE_WHOLE_MSG =  DACCOMPMS_K_SIZE_HEADER
                                             + DACCOMPMS_K_SIZE_CRC;

const unsigned short DACCOMPMS_K_BYTE_SYSTEM_ID = 12; // Position of the system id
                                               // byte in a table
const unsigned short DACCOMPMS_K_BYTE_TABLE_ID  = 13; // Position of the table id
                                               // byte in a table
const unsigned short DACCOMPMS_K_BYTE_DATA_TYPE = 14; // Position of the table data
                                               // type  byte in a table
const unsigned short DACCOMPMS_K_BYTE_ADDRESS = 21; // Position of the address field
                                               // type  byte in a table
const unsigned short DACCOMPMS_K_WORD_TABLE_SIZE = 23; // Position of the MSB for the word
                                               // containing the size of a table

void StoreFileName(int argc, char *argv[])
{
    if(argc == 4)
    {
        SpyLogFileName = argv[1];
        ExcFileName = argv[2];
        EvarFileName = argv[3];
    }
    else
    {
        PrintUsage(argv);
    }
}

void PrintUsage(char **argv)
{
    (void) argv;

    cout << "Usage: " << "Spylog_decoder " << " "
         << "<Spylog file> "
         << "<Exchange file> "
         << "<Evariable file>"
         << endl << endl;
    cout << "\tSpylog file - Please use the online file" << endl;
    cout << "\tExchange file - Please use the correct file for that environment" << endl;
    cout << "\tEvariable file - Please use the correct file for that environment" << endl;
    exit(0);
}

void ProcessDO(string strSystemId, string strTableId)
{
    // Get the address of the data
    unsigned short  usAddressInBits;
    unsigned short  usAddressInByte;
    unsigned short  usStartingAdressInByte;
    unsigned short  usRemainder;
    char            szAddress[3];
    stringstream key;


    // reset the name to empty
    EquName = "Not supported";

    // convert the address into unsigned short
    sprintf(szAddress,"%x%x",auiData[DACCOMPMS_K_BYTE_ADDRESS]
             ,auiData[DACCOMPMS_K_BYTE_ADDRESS+1]);
    usAddressInBits = strtoul(szAddress,NULL,16);
    //cout << "Starting AddressInBits: " << usAddressInBits << endl;
    usAddressInByte = usAddressInBits/8;
    //cout << "Starting AddressInByte: " << usAddressInByte << endl;
    usRemainder = usAddressInBits%8;
    //cout << "Starting Offset: " << usRemainder << endl;


    if(!ExcDataSet.IsKeyAvailable(strSystemId))
    {
        cout << "Starting not in exchange file" << endl;
        cout << "Equipment name: \"??\"" << endl;
        return;
    }
    else
    {
        usStartingAdressInByte =
                ExcDataSet.GetValueByKey(strSystemId)->
                GetTableStartAddress(atoi(strTableId.c_str()));
    }

    ByteAndBitPosController
                Data((usAddressInByte - usStartingAdressInByte - 18/* header size */),7);        
    Data.ShiftByBits(usRemainder);
    Data.SetDataLen(uiDataLength);

    //cout << endl << Data.GetBytePos() << " " << Data.GetBitPos() << endl;
    // Generate the hash key

    key.str("");
    key << auiData[DACCOMPMS_K_BYTE_SYSTEM_ID]
           << "_"
           << auiData[DACCOMPMS_K_BYTE_TABLE_ID]
              << "_"
              << Data.GetBytePos()
              << "_"
              << Data.GetBitPos();

    //cout << "Key used : " << key.str().c_str() << endl;

    if(EvarDataSet.IsKeyAvailableDO(key.str()) == true)
        EquName = EvarDataSet.GetValueByKeyDO(key.str())->GetEquipmentName();
    else
        EquName = "Not found or not supported";

    cout << "Equipment name: \"" << EquName.c_str() << "\"" << endl;
}

unsigned int CalculateData(unsigned int i_uiStartByte,
                           unsigned int i_uiStartBit,
                           unsigned int i_uiBitLength)
{
    const unsigned int uiByte0Index = DACCOMPMS_K_WORD_TABLE_SIZE + 2;
    unsigned char ucMask = 0x00;
    unsigned char ucData = (unsigned char)auiData[uiByte0Index+i_uiStartByte];

    ucData >>= i_uiStartBit;

    // create the mask char
    for(size_t c = 0; c < i_uiBitLength; c++)
    {
        ucMask <<= 1;
        ucMask = (ucMask | 0x01);
    }

    ucData = ucData & ucMask;

    return (unsigned int)ucData;
}

void ProcessDI(string strSystemId, string strTableId)
{
    unsigned int uiData;
    char szBuffer[256];

    printf("%s;%s/%s/%s/%s/%s;   %s\n",
        "Equipment Name",
        "SystemID",
        "TableID",
        "ByteNo",
        "StartBit",
        "BitLength",
        "Data"
        );

    for(size_t uiCount = 0; uiCount < EvarDataSet.GetEvarDataSetVecSize(); uiCount++)
    {
        //////////////////
        // Calculate data
        //////////////////

        // Only process the system ID corresponding to this spy message
        if(EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetSystemID() == atoi(strSystemId.c_str()) &&
           EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetTableNo() == atoi(strTableId.c_str())
                )
        {

            uiData = CalculateData(
                        EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetByteNo(),
                        EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetStartBit(),
                        EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetBitLength()
                        );

            sprintf(szBuffer,"%s;%03d/%03u/%05u/%u/%06u",
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetEquipmentName().c_str(),
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetSystemID(),
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetTableNo(),
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetByteNo(),
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetStartBit(),
                EvarDataSet.GetEvarDataSetVecByIndex(uiCount)->GetBitLength()
                );

            printf("%-60s %-u\n",szBuffer,uiData);
        }
    }
}

void Displaydata()
{

    TABLE_TYPE eTable_type;
    char szSystemId[128];
    char szTableId[128];

    // This type of message dont satisfy the protocol requirement
    if(auiData[6] == 0xc0)
    {
        return;
    }

    // print header msg
    cout << szMsgHdr << endl;

    // print slave address
    {
        char szBuffer[128];
        if(auiData[0] == kSLAVE_NUM_SR)
            strcpy(szBuffer, "Server (Server -> RTU)");
        else if(auiData[0] == kSLAVE_NUM_RS)
            strcpy(szBuffer, "PMS (RTU -> Server)");
        else
            strcpy(szBuffer, "Unknown (??)");

        cout << "Slave Address : " << szBuffer << endl;
    }

    // print function code
    {
        char szBuffer[128];
        sprintf(szBuffer, "0x%02X or %d(decimal)",auiData[1],auiData[1]);

        if(auiData[1] == kWRITE_N_WORDS)
            strcpy(szBuffer, "Modbus Write (in WORDS)");
        else if(auiData[1] == kREAD_N_WORDS)
            strcpy(szBuffer, "Modbus Read (in WORDS)");
        else if(auiData[1] == kWRITE_N_BITS)
            strcpy(szBuffer, "Modbus Write (in BITS)");
        else
            strcpy(szBuffer, "Unknown (??)");

        cout << "Function Code : " << szBuffer << endl;
    }

    // print sequence number (Not using at the moment)

    // print server ID (Not using at the moment)

    // print system ID
    {
        char szBuffer[128];
        sprintf(szBuffer, "Unknown");

        if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kRTU_ID)
        {
            strcpy(szBuffer, "RTU SYSTEM TABLE");
            //return;
        }
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kSIGNALLING_ID)
            strcpy(szBuffer, "SIGNALLING");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPOWER_ID)
            strcpy(szBuffer, "POWER");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPOWER2_ID)
            strcpy(szBuffer, "POWER2");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPOWER3_ID)
            strcpy(szBuffer, "POWER3");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPIS_ID)
            strcpy(szBuffer, "PIS");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kCCTV_ID)
            strcpy(szBuffer, "CCTV");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kCLOCK_ID)
            strcpy(szBuffer, "CLOCK");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPAS_ID)
            strcpy(szBuffer, "PAS");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT1_ID)
            strcpy(szBuffer, "LIFT1");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT2_ID)
            strcpy(szBuffer, "LIFT2");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT3_ID)
            strcpy(szBuffer, "LIFT3");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT4_ID)
            strcpy(szBuffer, "LIFT4");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT5_ID)
            strcpy(szBuffer, "LIFT5");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kLIFT6_ID)
            strcpy(szBuffer, "LIFT6");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kESC_ID)
            strcpy(szBuffer, "ESC");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kECS_ID)
            strcpy(szBuffer, "ECS");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kFIRE_ID)
            strcpy(szBuffer, "FIRE");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kWASH_ID)
            strcpy(szBuffer, "WASH");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPLC1_ID)
            strcpy(szBuffer, "PLC1");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPLC2_ID)
            strcpy(szBuffer, "PLC2");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPLC3_ID)
            strcpy(szBuffer, "PLC3");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPLC4_ID)
            strcpy(szBuffer, "PLC4");
        else if(auiData[DACCOMPMS_K_BYTE_SYSTEM_ID] == kPLC5_ID)
            strcpy(szBuffer, "PLC5");
        cout << "System ID     : " << szBuffer << endl;

        sprintf(szSystemId, "%u", auiData[DACCOMPMS_K_BYTE_SYSTEM_ID]);
    }

    // print table number
    {
        char szBuffer[128];
        sprintf(szBuffer, "0x%02X or %02d(decimal)",auiData[DACCOMPMS_K_BYTE_TABLE_ID]
                ,auiData[DACCOMPMS_K_BYTE_TABLE_ID]);

        cout << "Table Number  : " << szBuffer << endl;      
        sprintf(szTableId, "%u", auiData[DACCOMPMS_K_BYTE_TABLE_ID]);
    }

    // print table type
    {
        char szBuffer[128];
        sprintf(szBuffer, "Unknown");

        if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_EVENT)
        {
            strcpy(szBuffer, "Event table");
                eTable_type = event;
        }
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_DI)
        {
            strcpy(szBuffer, "DI table");
            eTable_type = DI;
        }
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_AI)
            strcpy(szBuffer, "AI table");
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_MI)
            strcpy(szBuffer, "MI (metering input) table");
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_DI8)
        {
            strcpy(szBuffer, "DI8 table");
            eTable_type = DI8;
        }
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_SI)
            strcpy(szBuffer, "SI table");
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_DO)
        {
            strcpy(szBuffer, "DO table");
            eTable_type = DO;
        }
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_AO)
            strcpy(szBuffer, "AO table");
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_DO8)
        {
            strcpy(szBuffer, "DO8 table");
            eTable_type = DO8;
        }
        else if(auiData[DACCOMPMS_K_BYTE_DATA_TYPE] == DACCOMPMS_K_TABLE_SO)
            strcpy(szBuffer, "SO table");

        cout << "Table Type    : " << szBuffer << endl;
    }

    // print table size
    {
        unsigned short usSize;
        char szBuffer[128];
        szBuffer[1] = auiData[DACCOMPMS_K_WORD_TABLE_SIZE];
        szBuffer[0] = auiData[DACCOMPMS_K_WORD_TABLE_SIZE+1];
        memcpy(&usSize,szBuffer,2);

        if(eTable_type == DO || eTable_type == DO8)
        {
            sprintf(szBuffer, "Data size     : %d bits",usSize);
        }
        else if(eTable_type == DI || eTable_type == DI8)
        {
            sprintf(szBuffer, "Data size     : %d bytes",usSize);
        }
        uiDataLength = usSize;
        cout << szBuffer << endl;
    }

    // Get the equipment type
    if(eTable_type == DO || eTable_type == DO8)
    {
        //cout << endl;
        ProcessDO(string(szSystemId), string(szTableId));

        // print data
        cout << "Table Data    : ";
        // Minus 2 to mask off the CRC.
        for(unsigned int c = DACCOMPMS_K_WORD_TABLE_SIZE+2, counter = 0; c < uiCount - 2; c++,counter++)
        {
            if((counter % 16) == 0)
            {
                cout << endl;
            }
            printf("%02X ",auiData[c]);
        }
    }
    // Get the equipment type
    if(eTable_type == DI || eTable_type == DI8)
    {
        //cout << endl;
        ProcessDI(string(szSystemId), string(szTableId));
    }
    else if(eTable_type == event)
    {
        cout << "Not supported in this version...\n";
    }

    cout << endl << endl;
}
