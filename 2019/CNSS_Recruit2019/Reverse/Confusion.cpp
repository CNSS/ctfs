#include<cstdio>     
#include<iostream>     
#include<vector>      
#include<cstring>
#include<windows.h>
#define LL long long     
#define WHITE SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),FOREGROUND_BLUE|FOREGROUND_GREEN|FOREGROUND_RED|FOREGROUND_INTENSITY);
#define RED SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),FOREGROUND_RED|FOREGROUND_INTENSITY);
#define GREEN SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),FOREGROUND_GREEN|FOREGROUND_INTENSITY);
#define BLUE SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE),FOREGROUND_BLUE|FOREGROUND_INTENSITY);
using namespace std;   

typedef struct
{
    unsigned int count[2];
    unsigned int state[4];
    unsigned char buffer[64];   
}MD5_CTX;
 
                         
#define F(x,y,z) ((x & y) | (~x & z))
#define G(x,y,z) ((x & z) | (y & ~z))
#define H(x,y,z) (x^y^z)
#define I(x,y,z) (y ^ (x | ~z))
#define ROTATE_LEFT(x,n) ((x << n) | (x >> (32-n)))
#define FF(a,b,c,d,x,s,ac) \
          { \
          a += F(b,c,d) + x + ac; \
          a = ROTATE_LEFT(a,s); \
          a += b; \
          }
#define GG(a,b,c,d,x,s,ac) \
          { \
          a += G(b,c,d) + x + ac; \
          a = ROTATE_LEFT(a,s); \
          a += b; \
          }
#define HH(a,b,c,d,x,s,ac) \
          { \
          a += H(b,c,d) + x + ac; \
          a = ROTATE_LEFT(a,s); \
          a += b; \
          }
#define II(a,b,c,d,x,s,ac) \
          { \
          a += I(b,c,d) + x + ac; \
          a = ROTATE_LEFT(a,s); \
          a += b; \
          }                                            
void MD5Init(MD5_CTX *context);
void MD5Update(MD5_CTX *context,unsigned char *input,unsigned int inputlen);
void MD5Final(MD5_CTX *context,unsigned char digest[16]);
void MD5Transform(unsigned int state[4],unsigned char block[64]);
void MD5Encode(unsigned char *output,unsigned int *input,unsigned int len);
void MD5Decode(unsigned int *output,unsigned char *input,unsigned int len);
 
unsigned char PADDING[]={0x80,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
                         
void MD5Init(MD5_CTX *context)
{
     context->count[0] = 0;
     context->count[1] = 0;
     context->state[0] = 0x67452301;
     context->state[1] = 0xEFCDAB89;
     context->state[2] = 0x98BADCFE;
     context->state[3] = 0x10325476;
}
void MD5Update(MD5_CTX *context,unsigned char *input,unsigned int inputlen)
{
    unsigned int i = 0,index = 0,partlen = 0;
    index = (context->count[0] >> 3) & 0x3F;
    partlen = 64 - index;
    context->count[0] += inputlen << 3;
    if(context->count[0] < (inputlen << 3))
       context->count[1]++;
    context->count[1] += inputlen >> 29;
    
    if(inputlen >= partlen)
    {
       memcpy(&context->buffer[index],input,partlen);
       MD5Transform(context->state,context->buffer);
       for(i = partlen;i+64 <= inputlen;i+=64)
           MD5Transform(context->state,&input[i]);
       index = 0;        
    }  
    else
    {
        i = 0;
    }
    memcpy(&context->buffer[index],&input[i],inputlen-i);
}
void MD5Final(MD5_CTX *context,unsigned char digest[16])
{
    unsigned int index = 0,padlen = 0;
    unsigned char bits[8];
    index = (context->count[0] >> 3) & 0x3F;
    padlen = (index < 56)?(56-index):(120-index);
    MD5Encode(bits,context->count,8);
    MD5Update(context,PADDING,padlen);
    MD5Update(context,bits,8);
    MD5Encode(digest,context->state,16);
}
void MD5Encode(unsigned char *output,unsigned int *input,unsigned int len)
{
    unsigned int i = 0,j = 0;
    while(j < len)
    {
         output[j] = input[i] & 0xFF;  
         output[j+1] = (input[i] >> 8) & 0xFF;
         output[j+2] = (input[i] >> 16) & 0xFF;
         output[j+3] = (input[i] >> 24) & 0xFF;
         i++;
         j+=4;
    }
}
void MD5Decode(unsigned int *output,unsigned char *input,unsigned int len)
{
     unsigned int i = 0,j = 0;
     while(j < len)
     {
           output[i] = (input[j]) |
                       (input[j+1] << 8) |
                       (input[j+2] << 16) |
                       (input[j+3] << 24);
           i++;
           j+=4; 
     }
}
void MD5Transform(unsigned int state[4],unsigned char block[64])
{
     unsigned int a = state[0];
     unsigned int b = state[1];
     unsigned int c = state[2];
     unsigned int d = state[3];
     unsigned int x[64];
     MD5Decode(x,block,64);
     FF(a, b, c, d, x[ 0], 7, 0xd76aa478); /* 1 */
 FF(d, a, b, c, x[ 1], 12, 0xe8c7b756); /* 2 */
 FF(c, d, a, b, x[ 2], 17, 0x242070db); /* 3 */
 FF(b, c, d, a, x[ 3], 22, 0xc1bdceee); /* 4 */
 FF(a, b, c, d, x[ 4], 7, 0xf57c0faf); /* 5 */
 FF(d, a, b, c, x[ 5], 12, 0x4787c62a); /* 6 */
 FF(c, d, a, b, x[ 6], 17, 0xa8304613); /* 7 */
 FF(b, c, d, a, x[ 7], 22, 0xfd469501); /* 8 */
 FF(a, b, c, d, x[ 8], 7, 0x698098d8); /* 9 */
 FF(d, a, b, c, x[ 9], 12, 0x8b44f7af); /* 10 */
 FF(c, d, a, b, x[10], 17, 0xffff5bb1); /* 11 */
 FF(b, c, d, a, x[11], 22, 0x895cd7be); /* 12 */
 FF(a, b, c, d, x[12], 7, 0x6b901122); /* 13 */
 FF(d, a, b, c, x[13], 12, 0xfd987193); /* 14 */
 FF(c, d, a, b, x[14], 17, 0xa679438e); /* 15 */
 FF(b, c, d, a, x[15], 22, 0x49b40821); /* 16 */
 
 /* Round 2 */
 GG(a, b, c, d, x[ 1], 5, 0xf61e2562); /* 17 */
 GG(d, a, b, c, x[ 6], 9, 0xc040b340); /* 18 */
 GG(c, d, a, b, x[11], 14, 0x265e5a51); /* 19 */
 GG(b, c, d, a, x[ 0], 20, 0xe9b6c7aa); /* 20 */
 GG(a, b, c, d, x[ 5], 5, 0xd62f105d); /* 21 */
 GG(d, a, b, c, x[10], 9,  0x2441453); /* 22 */
 GG(c, d, a, b, x[15], 14, 0xd8a1e681); /* 23 */
 GG(b, c, d, a, x[ 4], 20, 0xe7d3fbc8); /* 24 */
 GG(a, b, c, d, x[ 9], 5, 0x21e1cde6); /* 25 */
 GG(d, a, b, c, x[14], 9, 0xc33707d6); /* 26 */
 GG(c, d, a, b, x[ 3], 14, 0xf4d50d87); /* 27 */
 GG(b, c, d, a, x[ 8], 20, 0x455a14ed); /* 28 */
 GG(a, b, c, d, x[13], 5, 0xa9e3e905); /* 29 */
 GG(d, a, b, c, x[ 2], 9, 0xfcefa3f8); /* 30 */
 GG(c, d, a, b, x[ 7], 14, 0x676f02d9); /* 31 */
 GG(b, c, d, a, x[12], 20, 0x8d2a4c8a); /* 32 */
 
 /* Round 3 */
 HH(a, b, c, d, x[ 5], 4, 0xfffa3942); /* 33 */
 HH(d, a, b, c, x[ 8], 11, 0x8771f681); /* 34 */
 HH(c, d, a, b, x[11], 16, 0x6d9d6122); /* 35 */
 HH(b, c, d, a, x[14], 23, 0xfde5380c); /* 36 */
 HH(a, b, c, d, x[ 1], 4, 0xa4beea44); /* 37 */
 HH(d, a, b, c, x[ 4], 11, 0x4bdecfa9); /* 38 */
 HH(c, d, a, b, x[ 7], 16, 0xf6bb4b60); /* 39 */
 HH(b, c, d, a, x[10], 23, 0xbebfbc70); /* 40 */
 HH(a, b, c, d, x[13], 4, 0x289b7ec6); /* 41 */
 HH(d, a, b, c, x[ 0], 11, 0xeaa127fa); /* 42 */
 HH(c, d, a, b, x[ 3], 16, 0xd4ef3085); /* 43 */
 HH(b, c, d, a, x[ 6], 23,  0x4881d05); /* 44 */
 HH(a, b, c, d, x[ 9], 4, 0xd9d4d039); /* 45 */
 HH(d, a, b, c, x[12], 11, 0xe6db99e5); /* 46 */
 HH(c, d, a, b, x[15], 16, 0x1fa27cf8); /* 47 */
 HH(b, c, d, a, x[ 2], 23, 0xc4ac5665); /* 48 */
 
 /* Round 4 */
 II(a, b, c, d, x[ 0], 6, 0xf4292244); /* 49 */
 II(d, a, b, c, x[ 7], 10, 0x432aff97); /* 50 */
 II(c, d, a, b, x[14], 15, 0xab9423a7); /* 51 */
 II(b, c, d, a, x[ 5], 21, 0xfc93a039); /* 52 */
 II(a, b, c, d, x[12], 6, 0x655b59c3); /* 53 */
 II(d, a, b, c, x[ 3], 10, 0x8f0ccc92); /* 54 */
 II(c, d, a, b, x[10], 15, 0xffeff47d); /* 55 */
 II(b, c, d, a, x[ 1], 21, 0x85845dd1); /* 56 */
 II(a, b, c, d, x[ 8], 6, 0x6fa87e4f); /* 57 */
 II(d, a, b, c, x[15], 10, 0xfe2ce6e0); /* 58 */
 II(c, d, a, b, x[ 6], 15, 0xa3014314); /* 59 */
 II(b, c, d, a, x[13], 21, 0x4e0811a1); /* 60 */
 II(a, b, c, d, x[ 4], 6, 0xf7537e82); /* 61 */
 II(d, a, b, c, x[11], 10, 0xbd3af235); /* 62 */
 II(c, d, a, b, x[ 2], 15, 0x2ad7d2bb); /* 63 */
 II(b, c, d, a, x[ 9], 21, 0xeb86d391); /* 64 */
     state[0] += a;
     state[1] += b;
     state[2] += c;
     state[3] += d;
}

struct bigint{     
    static const int base=1000000000;     
    static const int width=9;     
    vector<LL>s;     
    bigint (LL num=0){*this=num;}     
    bigint operator = (LL num){     
        s.clear();     
        do{     
            s.push_back(num%base);     
            num/=base;     
        }while(num>0);     
        return *this;     
    }     
    bigint operator = (const string& str){     
        s.clear();     
        int x,len=(str.length()-1)/width+1;     
        for(int i=0;i<len;i++){     
            int end=str.length()-i*width;     
            int start=max(0,end-width);     
            sscanf(str.substr(start,end-start).c_str(),"%d",&x);     
            s.push_back(x);     
        }     
        return *this;     
    }     
    bigint operator + (const bigint& b) const{     
        bigint c;     
        c.s.clear();     
        for(int i=0,g=0;;i++){     
            if(g==0&&i>=s.size()&&i>=b.s.size())break;     
            int x=g;     
            if(i<s.size())x+=s[i];     
            if(i<b.s.size())x+=b.s[i];     
            c.s.push_back(x%base);     
            g=x/base;     
        }     
        return c;     
    }     
    bigint operator - (const bigint& b) const{     
        bigint c;     
        c.s.clear();     
        for(int i=0,g=0;;i++){     
            if(g==0&&i>=s.size())break;     
            int x=g;     
            if(i<s.size())x+=s[i];     
            if(i<b.s.size())x-=b.s[i];     
            if(x<0)x+=base,g=-1;     
            else g=0;     
            c.s.push_back(x);     
        }     
        return c;     
    }  
    bigint operator * (const bigint& b) const{  
        bigint c;  
        c.s.clear();  
        LL i,j,g;  
        LL temp,temp1;  
        c.s.resize(s.size()+b.s.size());  
        for(i=0;i<s.size();i++){  
            g=0,temp1=0;  
            for(j=0;j<b.s.size();j++){  
                LL x=c.s[i+j];  
                temp=s[i]*b.s[j]+g;  
                g=temp/base;  
                x+=temp%base+temp1;  
                temp1=x/base;  
                x%=base;  
                c.s[i+j]=x;  
            }  
            if(g!=0)  
                c.s[i+j]=g;  
        }  
        if(temp1!=0)  
            c.s[i+j]=temp1;  
        while(c.s.back()==0&&c.s.size()>1)  
            c.s.pop_back();  
        return c;  
    }  
    bool operator < (const bigint&b) const{     
        if(s.size()!=b.s.size())return s.size()<b.s.size();     
        for(int i=s.size()-1;i>=0;i--)     
            if(s[i]!=b.s[i])return s[i]<b.s[i];     
        return false;     
    }     
    bool operator > (const bigint&b) const{return b<*this;}     
    bool operator <= (const bigint&b) const{return !(b<*this);}     
    bool operator >= (const bigint&b) const{return !(*this>b);}     
    bool operator != (const bigint&b) const{return b<*this|| *this<b;}     
    bool operator == (const bigint&b) const{return !(b<*this)&&!(*this<b);}
	bigint operator *= (const bigint &b){*this=(*this)*b; return *this;}     
    bigint operator -= (const bigint &b){*this=(*this)-b; return *this;}  
    bigint operator += (const bigint &b){*this=(*this)+b; return *this;}   
    bigint operator ++ (int){*this=*this+1; return *this;}   
    bigint& operator ++ () {*this=*this+1; return *this;}  
    bigint operator -- (int){*this=*this-1; return *this;}   
    bigint& operator -- (){*this=*this-1; return *this;}       
}encode[50];     

LL Encode_flag[]={0x63,0x6F,0x71,0x76,0x77,0x5A,0x59,0x6F,0x2C,0x7F,0x5B,0x6A,0x29,0x72,0x66,0x83,0x21,0x76,0x52,0x72,0x2D,0x74,0x52,0x78,0x3A,0x7D,0x45,0x62,0x45,0x8A,0x15,0x9C};
ostream& operator << (ostream &out,const bigint& x){     
    out<<x.s.back();     
    for(int i=x.s.size()-2;i>=0;i--){     
        char buf[20];     
        sprintf(buf,"%09d",x.s[i]);     
        for(int j=0;j<strlen(buf);j++)out<<buf[j];         
    }     
    return out;     
}     
istream& operator >> (istream &in,bigint&x){     
    string s;     
    if(!(in>>s))return in;     
    x=s;     
    return in;     
}
unsigned char str[50];
unsigned char true_flag[50];
char CNSS[]="cnss{";
unsigned char decrypt[16];
unsigned char decrypt_flag[16];

void Right(){
	GREEN
	puts("And finally, you got how to reverse smartly~");
}
void Wrong(){
	RED
	puts("But you get lost in it....");
}
void check_1(){
	if(strlen((char *)str)!=32){
		Wrong();
		exit(0);
	}
}
void check_2(){
	char temp[50]={0};
	int Flag=1;
	for(int i=0;i<5;i++)
		if(str[i]!=CNSS[i])Flag=0;
	if(!Flag){
		Wrong();
		exit(0);
	}
}
void Encode_input(){
	MD5_CTX md5;
	MD5Init(&md5);         		
	MD5Update(&md5,str,strlen((char *)str));
	MD5Final(&md5,decrypt); 
}
void Init(){
	for(int i=0;i<32;i++)
		encode[i]=Encode_flag[i];
}
void Decode_flag(){
	Init();
	for(int i=0;i<32;i++){
		bigint temp=(LL)i;
		if(i&1){
			encode[i]=encode[i]-temp;
		}
		else {
			encode[i]=encode[i]+temp;
		}
	}
	cout<<endl;
	for(int i=0;i<32;i++){
		int ans;
		for(int j=33;j<127;j++){
			bigint temp=(LL)j;
			if(temp==encode[i]){
				ans=j;
				break;
			}
		}
		true_flag[i]=(unsigned char)ans;
	}
}
void Encode_Flag(){
	MD5_CTX md5;
	MD5Init(&md5);         		
	MD5Update(&md5,true_flag,strlen((char *)true_flag));
	MD5Final(&md5,decrypt_flag); 
}
bool mystrcmp(unsigned char *a,unsigned char *b){
	for(int i=0;i<16;i++)
		if(a[i]!=b[i])return 0;
	return 1;
}
void HideCursor()
{
    CONSOLE_CURSOR_INFO cursor_info = {1, 0};
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);
}
void Gotoxy(int x, int y)
{
    HANDLE hout; 
    COORD coord; 
    coord.X = x;
    coord.Y = y;
    hout = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorPosition(hout, coord);
}

char welcome1[]="One day, SuperGate told you that once you input the right key, the door of reversing will open. \nSo you tried over and over again. And at last you submitted your key:\n";
void DrawUi(){
	int len;
    HideCursor();
    for(len = 1; len <= 25; len++){
        Gotoxy(2 * len, 1    );
        printf("█");
        Gotoxy(21, 4);
        printf("Problem downloading..%d%%", 4 * len);
        Sleep(100);
    }
    Gotoxy(21, 4);
    printf("Download successfully....\n\n");
    for(int i=0;i<strlen(welcome1);i++){
    	BLUE
    	putchar(welcome1[i]);
    	Sleep(40);
	}
}

int main(){  
	system("cls");
	DrawUi();
    bigint a,b;
    WHITE
    scanf("%s",str);
   	check_1();
   	check_2();
   	Decode_flag();
   	Encode_input();
   	Encode_Flag();
	if(mystrcmp(decrypt_flag,decrypt))Right();
	else Wrong();
	WHITE
}  
