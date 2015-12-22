#ifndef DWLDATA_H
#define DWLDATA_H

#include "Global_header.h"
#include "Global.h"

struct TableData
{
    unsigned int uiTableId;
    unsigned int uiStartAddress;
    unsigned int uiEndAddress;
};

class ExcData
{
public:

    // Accessor methods
    virtual unsigned int GetTableStartAddress(unsigned int i_uiTableId) const
    {
        for(unsigned int c = 0;  c < TableDataSet_.size(); c++)
        {
            if(TableDataSet_[c]->uiTableId == i_uiTableId)
                return TableDataSet_[c]->uiStartAddress;
        }
        return -1;
    }

    virtual unsigned int GetSystemID() const
    {
        return usSystemID_;
    }

    // Mutator methods
    virtual void SetTableData(TableData* i_TableData)
    {
        TableDataSet_.push_back(i_TableData);
    }

    virtual void SetSystemID(unsigned int i_usSystemID)
    {
        usSystemID_ = i_usSystemID;
    }

private:

    unsigned int  usSystemID_;
    vector<TableData*> TableDataSet_;
};

class ExcDataMgr
{
public:

    void StoreExcDataMgr(string i_strData)
    {
        char *pToken;
        //char szbuffer[2056];
        char szbuffer2[256];
        ExcData *ExcDataEntry;
        TableData *TableDataEntry;
        string strBuffer4;
        stringstream strstreambuffer3;

        // Only process System line
        if(i_strData.find("System",0,6) == string::npos)
            return;


        // Take away "System="
        //strcpy(szbuffer,i_strData.substr(i_strData.find_first_of('=')).c_str()+1);

        std::string szbuffer;
        szbuffer = i_strData.substr(i_strData.find_first_of('='));

        std::cout << "szbuffer: " << szbuffer << std::endl;

        // Trim all white space off for easy processing
        TrimChar(szbuffer);
        std::cout << "szbuffer: " << szbuffer << std::endl;

        // Trim the last ',' away
        /* if(szbuffer[strlen(szbuffer)-1] == ',') */
        /*     szbuffer[strlen(szbuffer)-1] = '\0'; */
        szbuffer.erase(szbuffer.find_last_of(','), -1);
        std::cout << "szbuffer: " << szbuffer << std::endl;

        ExcDataEntry = new ExcData;

        // Separate all the fields
        char *buffer = new char[szbuffer.length() + 1];
        strcpy(buffer, szbuffer.c_str());

        pToken = strtok(buffer, ",");
        std::cout << "pToken (0): " << pToken << std::endl;
        
        // First field
        // Not interested in this field.
        pToken = strtok(NULL, ",");
        std::cout << "pToken (1): " << pToken << std::endl;

        // Second field
        ExcDataEntry->SetSystemID(strtoul(pToken,NULL,16));
        pToken = strtok(NULL, ",");
        std::cout << "pToken (2): " << pToken << std::endl;

        // third field
        // Not interested in this field.
        pToken = strtok(NULL, ",");
        std::cout << "pToken (3): " << pToken << std::endl;

        // fourth field
        // Not interested in this field.
        //cout << pToken << endl;
        pToken = strtok(NULL, ",");

        // fifth field
        TrimChar(pToken,'(');
        strcpy(szbuffer,pToken);

        // Break the uplist
        pToken = strtok(szbuffer, ")");
        while(pToken != NULL)
        {
            strcpy(szbuffer2,pToken);
            ReplaceChar(szbuffer2, ';', ' ');

            TableDataEntry = new TableData;
            sscanf(szbuffer2, "%d %*d %x  %x", &TableDataEntry->uiTableId,
                    &TableDataEntry->uiStartAddress,
                    &TableDataEntry->uiEndAddress);

            ExcDataEntry->SetTableData(TableDataEntry);
            pToken = strtok(NULL, ")");
        }

        // input to buffer
        strstreambuffer3 << ExcDataEntry->GetSystemID();
        strBuffer4 = strstreambuffer3.str();
        ExcDataSet_[strBuffer4] = ExcDataEntry;
    }

    ExcData* GetValueByKey(string i_key) const
    {
        return ExcDataSet_.at(i_key);
    }

    bool IsKeyAvailable(string i_key)
    {
        if(ExcDataSet_.count(i_key) == 1)
            return true;
        else
            return false;
    }

private:
    
    void TrimChar(std::string& i_pData, const char cChar = ' ') {
      i_pData.erase(i_pData.find(cChar));
    }

    /* void TrimChar(char * i_pData, char cChar = ' ') */
    /* { */
    /*     // trim all space off */
    /*     for(int c = 0;; c++) */
    /*     { */
    /*         if((i_pData[c]) == cChar) */
    /*         { */
    /*             if(i_pData[c+1] != '\0') */
    /*                 strcpy(i_pData+c,i_pData+c+1); */
    /*         } */
    /*         if(i_pData[c] == '\0') */
    /*             break; */
    /*     } */
    /* } */

    void ReplaceChar(char * i_pData, char cFromChar, char cToChar)
    {
        for(size_t c = 0; c < strlen(i_pData); c++)
            if(i_pData[c] == cFromChar)
                i_pData[c] = cToChar;
    }

    map<string, ExcData*> ExcDataSet_;
};

#endif // DWLDATA_H
