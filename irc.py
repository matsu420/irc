#!/usr/bin/env python

import sys, socket, os


TARGET = "localhost"
PORT = "6667"

BUF_SIZE = 1024


def irc_connect(irc_socket, target, port):
    irc_socket.connect((target, port))


def login(irc_server, nickname, username, realname, hostname = "hostname", servername = "servername"):
    nick_message = "NICK " + nickname + "\n"
    user_message = "USER %s %s %s :%s" % (username, hostname, servername, realname)
    user_message += "\n"

    irc_server.send(nickname)
    irc_server.send(username)


def join(irc_server, channel):
    join_message = "JOIN " + channel + "\n"

    irc_server.send(join_message)


def pong(irc_server, daemon, daemon2 = None):
    pong_message = "PONG %s %s" % (daemon, damon2)
    pong_message += "\n"

    irc_server.send(pong_message)


def privmsg(irc_server, channel, text):
    privmsg_message = "PRIVMSG %s :%s\n", % (channel, text)

    irc_server.send(privmsg_message)


def quit(irc_server):
    None


def handle_privmsg(prefix, receiver, text):
    print ""
    print prefix + ">" + text


def wait_message(irc_server):
    while(True):
        msg_buf = irc_server.recv(BUF_SIZE)
        messages = msg_buf.split()


        prefix = None
        temp = messages[0].strip()
        if temp[0] == ":":
            prefix = temp 
            messages = messages[1:]

        command = messages[0]
        params = messages[1:]

        if command == "PING":
            pong(irc_server, params[0])
        elif command == "PRIVMSG":
            text = ""
            receiver = ""
            for param in params:
                temp = param.strip()
                if temp[0] == ":":
                    text = temp[1:]
                else:
                    receiver = temp

            handle_privmsg(receiver, text)


def client_interface(irc_server, channel, prompt = ">"):
    while(True):
        print prompt.
        line = raw_input()

        if line == "quit":
            quit(irc_server)
            sys.exit(0)

        privmsg(irc_server, channel, line)


def main():
    nickname = "nickhoge"
    username = "hoge"
    realname = "hogehoge"
    channel = "#test_channel"

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_connect(irc, TARGET, PORT)

    login(irc, nickname, username, realname)

    join(irc, channel)

    pid = os.fork()

    if(pid == 0):#child
        wait_message(irc)
    else:
        client_interface(irc, channel)


if __name__ == "__main__":
    main()
