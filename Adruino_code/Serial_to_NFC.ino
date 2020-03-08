#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>


#include <Arduino.h>
#include <U8g2lib.h>

#define RST_PIN    D3   
#define SS_PIN     D8   
 
MFRC522 mfrc522(SS_PIN, RST_PIN); 

byte PSWBuff[] = {0xFF, 0xAB, 0xBA, 0xFF};
byte pACK[] = {0xE, 0x5};
byte WBuff[] = {0x00, 0x00, 0x00, 0x04};
byte RBuff[18];

void setup() {
  
  Serial.begin(9600);
  while (!Serial);
  SPI.begin();      
  mfrc522.PCD_Init();

}

void loop() {

 
String input = Serial.readString();

if (input == "IsNewCardPresent")
{
  Serial.println(mfrc522.PICC_IsNewCardPresent());
  
}
else if (input == "getID")
{
  Serial.println(getID());
}
else if (input =="ReadCredit")
{
  Serial.println(ReadCredit());
}
else if (input == "WriteCredit")
{
  Serial.println("Nr_of_credit?:");
  String Nr = Serial.readString();
  
  Serial.println(WriteCredit(Nr.toInt()));
}
else
{
  Serial.println("Err");
}

return; 

}


String getID()
{
  long code = 0;

  if (mfrc522.PICC_ReadCardSerial())
  {
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
      code = ((code + mfrc522.uid.uidByte[i]) * 10);
    }
  }
  return String(code, DEC);
}

int ReadCredit()
{
  byte buffer[18];
  byte byteCount;
  byteCount = sizeof(buffer);
  int res = mfrc522.MIFARE_Read(0x4, buffer, &byteCount);
  if (res != 0)
  {
    //Serial.println("Read Credit returns: Err code -1");
    return -1;
  }

  //Serial.println("Read Credit returns: " + String(buffer[1]));
  
  return (buffer[0]+buffer[1]+buffer[2]+buffer[3])/4; 
}

int WriteCredit(int newCredit_lokal)
{
  byte WBuff[] = {newCredit_lokal, newCredit_lokal, newCredit_lokal, newCredit_lokal};
  mfrc522.PCD_NTAG216_AUTH(&PSWBuff[0], pACK);
  return mfrc522.MIFARE_Ultralight_Write(0x4, WBuff, 4); 
}
