**About**

This is simple wow emulator for wow 2.4.3, developing from scratch for Linux (Mint, Cinnamon, 18.3 Sylvia).

Currently not works correctly, because client stucks on 'Connected'.
Debugging with wireshark shows that client stucks after SMSG_AUTH_RESPONSE.
Reason found: incorrect packet encrypting.

I'm using [MaNGOS-TBC](https://github.com/cmangos/mangos-tbc) and [DuratorEmu](https://github.com/Dece/DuratorEmu), [pywowd](https://github.com/fotcorn/pywowd) as Python examples.
Thanks a lot to developers for that projects ! 

Also thanks to [OwnedCore community](https://www.ownedcore.com) for help in debugging.

**Dependencies**

Currently there are no dependencies. You need `python3.5` to run this project.

**Before running**

Create databases from *DB/DB_List*. Then create tables from *DB/Fixtures*.

**Running**

Just go to the project root dir and run command from console `python3 Run.py`.
Also be sure realmlist.wtf (in your wow-client dir) is equals to `set realmlist localhost`.

**License**

You can fork this project or use current according to your needs (please, add the link to my repo, this will be very nice). 

Also you can be the contributor, if you want to help developing.
