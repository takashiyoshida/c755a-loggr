#ifndef EVARDATA_H
#define EVARDATA_H

#include "Global_header.h"
#include "Global.h"

class ByteAndBitPosController
{
public:

    ByteAndBitPosController(int i_iBytePos, int i_iBitPos)
    {
        iBytePos_ = i_iBytePos;
        iBitPos_ = i_iBitPos;
    }

    void ShiftByBits(int i_iNoOfBit)
    {
        int iNoOfBit = i_iNoOfBit;
        while(iNoOfBit--)
        {
            if(iBitPos_ == 0)
            {
                iBitPos_ = 7;
                iBytePos_++;
            }
            else
            {
                iBitPos_--;
            }
        }
    }
    void SetDataLen(int i_iNoOfBit)
    {
        int iNoOfBit = i_iNoOfBit - 1;
        ShiftByBits(iNoOfBit);
    }

    int GetBytePos() const
    {
        return iBytePos_;
    }
    int GetBitPos() const
    {
        return iBitPos_;
    }

private:

    int iBytePos_;
    int iBitPos_;
};

class EvarData
{
public:

    // Accessor methods
    virtual unsigned short GetSystemID() const
    {
        return usSystemID_;
    }
    virtual unsigned short GetTableNo() const
    {
        return usTableNo_;
    }
    virtual unsigned int GetByteNo() const
    {
        return uiByteNo_;
    }
    virtual unsigned short GetStartBit() const
    {
        return usStartBit_;
    }
    virtual unsigned short GetBitLength() const
    {
        return usBitLength_;
    }
    virtual string GetEquipmentName() const
    {
        return strEquipmentName_;
    }

    // Mutator methods
    virtual void SetSystemID(unsigned short i_usSystemID)
    {
        usSystemID_ = i_usSystemID;
    }
    virtual void SetTableNo(unsigned short i_usTableNo)
    {
        usTableNo_ = i_usTableNo;
    }
    virtual void SetByteNo(unsigned int i_uiByteNo)
    {
        uiByteNo_ = i_uiByteNo;
    }
    virtual void SetStartBit(unsigned short i_usStartBit)
    {
        usStartBit_ = i_usStartBit;
    }
    virtual void SetBitLength(unsigned short i_usBitLength)
    {
        usBitLength_ = i_usBitLength;
    }
    virtual void SetEquipmentName(string i_strEquipmentName)
    {
        strEquipmentName_ = i_strEquipmentName;
    }

private:

    unsigned short  usSystemID_;
    unsigned short  usTableNo_;
    unsigned int    uiByteNo_;
    unsigned short  usStartBit_;
    unsigned short  usBitLength_;
    string          strEquipmentName_;
};

class EvarDOData: public EvarData
{
public:

    enum DataType
    {
        DEOV
    };

    EvarDOData()
    {
        eDataType_ = DEOV;
    }

private:

    DataType        eDataType_;
};

class EvarDIData: public EvarData
{
public:

    enum DataType
    {
        DEIV
    };

    EvarDIData()
    {
        eDataType_ = DEIV;
    }

private:

    DataType        eDataType_;
};


static bool CompareIt (EvarData* First,EvarData* Second)
{
    return (First->GetByteNo() < Second->GetByteNo());
}

class EvarDataMgr
{
public:

    void StoreEvarDataMgr(string i_strData)
    {
        char *pToken;
        char buffer[1024];
        string strFields;
        EvarData *varDataEntry;
        stringstream key;

        strcpy(buffer,i_strData.c_str());

        pToken = strtok(buffer, ";");
        while (pToken != NULL)
        {
            // Process DEOV entry only
            if(strstr(pToken,"DEOV")!=0)
            {
                varDataEntry = new EvarDOData;

                // Start to break down all the fields
                strFields = pToken;

                if(strFields[6] != '$')
                {
                    varDataEntry->SetSystemID(atol(strFields.substr(6,3).c_str()));
                    //cout << varDataEntry->GetSystemID() << ' ';
                    varDataEntry->SetTableNo(atol(strFields.substr(10,3).c_str()));
                    //cout << varDataEntry->GetTableNo() << ' ';
                    varDataEntry->SetByteNo(atol(strFields.substr(14,5).c_str()));
                    //cout << varDataEntry->GetByteNo() << ' ';
                    varDataEntry->SetStartBit(atol(strFields.substr(20,1).c_str()));
                    //cout << varDataEntry->GetStartBit() << ' ';
                    varDataEntry->SetBitLength(atol(strFields.substr(22,6).c_str()));
                    //cout << varDataEntry->GetBitLength() << ' ';

                    // Get next field
                    pToken = strtok(NULL, ";");

                    // Store the equipment name
                    // shift pToken to take away the leading space
                    varDataEntry->SetEquipmentName(string(pToken+1));
                    //cout << varDataEntry->GetEquipmentName();
                    //cout << endl;

                    // Store to map
                    key.str("");
                    key << varDataEntry->GetSystemID() << "_"
                        << varDataEntry->GetTableNo() << "_"
                        << varDataEntry->GetByteNo() << "_"
                        << varDataEntry->GetStartBit();

                    EvarDataSet_[key.str()] = varDataEntry;
                    //cout << EvarDataSet_.size() << endl;
                }
                // Do not process entry with DEOV= $.......
                else
                {
                    break;
                }
            }
            // Process DEIV entry only
            if(strstr(pToken,"DEIV")!=0)
            {
                varDataEntry = new EvarDIData;

                // Start to break down all the fields
                strFields = pToken;

                if(strFields[6] != '$')
                {
                    varDataEntry->SetSystemID(atol(strFields.substr(6,3).c_str()));
                    //cout << varDataEntry->GetSystemID() << ' ';
                    varDataEntry->SetTableNo(atol(strFields.substr(10,3).c_str()));
                    //cout << varDataEntry->GetTableNo() << ' ';
                    varDataEntry->SetByteNo(atol(strFields.substr(14,5).c_str()));
                    //cout << varDataEntry->GetByteNo() << ' ';
                    varDataEntry->SetStartBit(atol(strFields.substr(20,1).c_str()));
                    //cout << varDataEntry->GetStartBit() << ' ';
                    varDataEntry->SetBitLength(atol(strFields.substr(22,6).c_str()));
                    //cout << varDataEntry->GetBitLength() << ' ';

                    // Get next field
                    pToken = strtok(NULL, ";");

                    // Store the equipment name
                    // shift pToken to take away the leading space
                    varDataEntry->SetEquipmentName(string(pToken+1));
                    //cout << varDataEntry->GetEquipmentName();
                    //cout << endl;

                    // Store to vector
                    EvarDataSetVec_.push_back(varDataEntry);
                }
                // Do not process entry with DEIV= $.......
                else
                {
                    break;
                }
            }
            else
            {
                pToken = strtok(NULL, ";");
            }
        }
    }

    EvarData* GetValueByKeyDO(string i_key)
    {
        return EvarDataSet_.at(i_key);
    }

    bool IsKeyAvailableDO(string i_key)
    {
        if(EvarDataSet_.count(i_key) == 1)
            return true;
        else
            return false;
    }

    size_t GetEvarDataSetVecSize() const
    {
        return EvarDataSetVec_.size();
    }

    EvarData* GetEvarDataSetVecByIndex(size_t i_uiIndex) const
    {
        return EvarDataSetVec_[i_uiIndex];
    }

    void SortVec()
    {
        sort(EvarDataSetVec_.begin(), EvarDataSetVec_.end(), CompareIt);
    }

private:



private:

    // DO and DO8 uses this map
    map<string, EvarData*> EvarDataSet_;

    // DI and DI8 uses this vector
    vector<EvarData*> EvarDataSetVec_;
};
#endif // EVARDATA_H
