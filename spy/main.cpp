#if 0
****************************************************************************
*                                                                            *
*  FILE             :                                                        *
*  FULL NAME        :                                                        *
*----------------------------------------------------------------------------*
*  AUTHOR           : Stanley Lim                                            *
*  COMPANY          :                                                        *
*  CREATION DATE    : Sep 19 2014                                            *
*  LANGUAGE         :                                                        *
*............................................................................*
*  OVERVIEW                                                                  *
*  The purpose of this program is to decode the spylog so that it is         *
*  it can be easier interpret by the user.                                   *
*............................................................................*
*  CONTENTS                                                                  *
*                                                                            *
*  1.1 (20 Oct 2014)  Stanley Lim                                            *
*      - Only support DO processing because it is improved to cater for ECS  *
*        issue.                                                              *
 ****************************************************************************
#endif
#include "Global_header.h"
#include "Global.h"


int main(int argc, char *argv[])
{

    (void) argc;

    fstream fs;
    string line;
    bool bStartOfMsgBlk;
    char *pTok;
    char szLine[512];

    // Get input file
    StoreFileName(argc, argv);

    // Open exchange File now
    fs.open(ExcFileName.c_str());
    if(fs.is_open())
    {
        while(getline(fs,line))
        {
            if(line.length() == 0 || line[0] == '#')
                continue;
            ExcDataSet.StoreExcDataMgr(line);
        }
        fs.close();
    }

    // Open Evar File now
    fs.open(EvarFileName.c_str());
    if(fs.is_open())
    {
        while(getline(fs,line))
        {
            if(line.length() == 0 || line[0] == '#')
                continue;
            EvarDataSet.StoreEvarDataMgr(line);
        }
        fs.close();

        // Sort is provided due to user feedback, for easy reading
        EvarDataSet.SortVec();
    }

    // Open spy log now
    fs.open(SpyLogFileName.c_str());
    if(fs.is_open())
    {
        bStartOfMsgBlk = false;
        
        // Get line from file
        while(getline(fs,line))
        {
            if(line.length() == 0)
            {
                bStartOfMsgBlk = false;
                // Start processing
                if(szMsgHdr[0] != '\0')
                {
                    Displaydata();
                    szMsgHdr[0] = '\0';
                }
                //cout << endl;
                continue;
            }

            // Get all the binary data
            if(bStartOfMsgBlk)
            {
                strcpy(szLine,line.c_str());

                // truncate the first words portion
                strcpy(szLine,szLine+4);

                // truncate the ascii portion
                szLine[string(szLine).find_first_of('\t')] = '\0';

                pTok = strtok(szLine," ");
                while (pTok != NULL)
                {
                    auiData[uiCurrentCount++] = strtol(pTok,NULL,16);
                    uiCount = uiCurrentCount;
                    pTok = strtok (NULL, " ");
                    //printf("%02X ",auiData[uiCurrentCount-1]);
                }
                //cout << endl;
                continue;
            }

            // check if this is the first line of message
            if(line.c_str()[2] == '/')
            {
                strcpy(szMsgHdr,line.c_str());
                bStartOfMsgBlk = true;
                uiCurrentCount = 0;
                uiCount = 0;
            }
        }
        fs.close();
    }

    return(0);
}


