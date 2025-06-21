when opening the directory i saw the passcode.c file and it had:

 printf("checking...\n");
        if(passcode1==123456 && passcode2==13371337){
                printf("Login OK!\n");
                setregid(getegid(), getegid());
                system("/bin/cat flag");
        }
        else{

so my assumption is i have to enter this as a passcode...
no ill try

conclusions:

if i enter more then 100chars at name theres stck overflow
if i enter a passcode 2 there is a stach overflow
passcode1 should be 123456 and passcode2 should be 13371337 both integers

i can enter them in the name but its a string

1337: \r%
123456: \n"8

when entering all fields i get seg fault. if i enter pass1 with " " in it its the same
also for username with " " " " in. so i need to find a way to enter all 3 fields with less then 3 " ":

but \0 and \n didnt work and somthing about the 1337 twice bothers me

