#!/usr/bin/env python

import sys, socket, os


TARGET = "localhost"
PORT = 6667

BUF_SIZE = 1024


def irc_connect(irc_socket, target, port):
    irc_socket.connect((target, port))


def login(irc_server, nickname, username, realname, hostname = "hostname", servername = "*"):
    nick_message = "NICK " + nickname + "\n"
    user_message = "USER %s %s %s :%s\n" % (username, hostname, servername, realname)


    irc_server.send(nick_message)
    irc_server.send(user_message)


def join(irc_server, channel):
    join_message = "JOIN " + channel + "\n"

    irc_server.send(join_message)


def pong(irc_server, daemon, daemon2 = None):
    pong_message = "PONG %s %s" % (daemon, daemon2)
    pong_message += "\n"

    irc_server.send(pong_message)


def privmsg(irc_server, channel, text):
    privmsg_message = "PRIVMSG %s :%s\n" % (channel, text)

    irc_server.send(privmsg_message)


def quit(irc_server):
    None


def handle_privmsg(prefix, receiver, text):
    print ""
    print prefix + ">" + text
    print ""


def wait_message(irc_server):
    while(True):
        msg_buf = irc_server.recv(BUF_SIZE)
        msg_buf = msg_buf.strip()

        prefix = None
        if msg_buf[0] == ":":
            p = msg_buf.find(" ")
            prefix = msg_buf[1:p]
            msg_buf = msg_buf[(p + 1):]

        p = msg_buf.find(":")
        if p != -1:#has last param which starts with ":"
            last_param = msg_buf[(p + 1):]
            msg_buf = msg_buf[:p]
            msg_buf = msg_buf.strip()

        messages = msg_buf.split()

        command = messages[0]
        params = messages[1:]

        if command == "PING":
            pong(irc_server, params[0])
        elif command == "PRIVMSG":
            text = last_param
            receiver = ""

            for param in params:
                receiver = param


            handle_privmsg(prefix, receiver, text)


def client_interface(irc_server, channel, prompt = ">"):
    while(True):
        print prompt,
        line = raw_input()

        if line == "quit":
            quit(irc_server)
            sys.exit(0)

        privmsg(irc_server, channel, line)


def main():
    nickname = "nickhoge"
    username = "usr"
    realname = "realname"
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
