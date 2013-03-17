Multiline-capable companion of /usr/bin/logger from bsdutils.

It will read the whole file of stdin and send it to syslog as one message.

It is supposed to be used with rsyslog, because rsyslog can handle bigger messages.
I will be using it to send cron job results to graylog.

I have configured rsyslog to escape newlines, accept longer messages and to forward them to graylog2:

    $EscapeControlCharactersOnReceive on
    $MaxMessageSize 65536

    local2.*        @@graylog2

On graylogs side I am unescaping the messages using the following drools: multiline-syslog.drl

Software used: rsyslog 4.6.4, graylog2-server 0.9.6
