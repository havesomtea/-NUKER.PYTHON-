# Nuker Bot
## Latest Alpha Version: v1.4-alpha
### This is the pre-release version; some features may be unstable or not work at all!
**Last STABLE version: v1.3.3**

**Here is the pre-release which is created when enough of the planned features are stable. It is available but I don't recommend you do unless you're feeling a little risky since many features can be unstable or broken.**

**Some features in these versions may never even be officially released and a pre-release is the only way to get them.**
**You may find requests and fixes from pull requests, issues, etc. in these versions.**
**All pre-release version will be officially released on the releases page but only Python files will be available.**

### Changes planned (will be ticked off when available in a PRE-RELEASE):
- A set of customisation options which allows you to configure how you want a nuke to work (e.g. you only want to delete all the channels or ban everyone). Example:
(all values are set to **true** by default and this command excludes giving you admin since there is !play)
!volume 1 false: disable deleting of all channels
(initiate the nuke) !skip: bans everyone, changes server icon and name, deletes all roles, makes the nuke channel **but does not delete any channels**
(note: this does not affect the classic !help nuke; this customisable nuke will be available in this command)


Planned customisation options:
~~Customisable nuking (as seen above)~~ Completed
~~Ability to customise the "get-nuked" channel into something else # Issue 2 @ QuantumFox42~~ Completed
~~Ability to customise the server name and icon~~ Completed
Ability to direct message all users before the nuke with a custom message (e.g. "GET NUKED!") # Issue 4 @ QuantumFox42

- Add support for bot tokens to be placed in .env files.

### Changes made from the last stable release (extends main/README.md so read that first)

### Commands
> !volume (config_option) (arguments): **customises the customisable nuke command !skip. Config options are 1-5 (you can also use * to select all options and supply True or False arguments to disable them) and accepted arguments are either "True" or "False" (case sensitive).**
**There is an exception for config option 5 of the nuke channel where you can specify True of False as well as a name for the channel. Example: !volume 5 True "lemon-channel". There is also another exception for config option 4 where you can specify a name and the name of the icon (if icon is in current directory, use "./" and if it is the parent directory, use "../"). Example: !volume 4 True "LEMON" "../lemon.jpg" (parent dir)**
Note: only .jpg files are supported.

> !skip: **nukes the server using the customisation options.**
