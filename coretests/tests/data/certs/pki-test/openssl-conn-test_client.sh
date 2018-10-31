#!/bin/bash

# OpenSSL test server for PKI connections

# LS 2017-05-25

# Tested against OpenSSL 1.0.2k

# Stand up test server
# See also (outdated): https://wiki.openssl.org/index.php/Manual:S_server(1)

set -e

# Set up boundless test certs for server and client authentication validation

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)
TEST_CERTS="$(dirname "${SCRIPT_DIR}")/certs-keys"

# Ensure whatever openssl needs launched is found first on PATH
# (here for Homebrew's keg-only openssl)
export PATH=/usr/local/opt/openssl/bin:$PATH

# use `openssl s_client --help` to verify specific options
# options in order of --help output

# Note: successful connections will end with prompt for an HTTP command, e.g.
# GET /
# if using -WWW on the test server, request:
# GET/test.html (returns contents of test.html)
openssl s_client -connect boundless.test:4443 \
  -verify 5 \
  -verify_return_error \
  -cert ${TEST_CERTS}/alice-cert.pem \
  -key ${TEST_CERTS}/alice-key.pem \
  -CAfile ${TEST_CERTS}/subissuer-issuer-root-ca_issuer-2-root-2-ca_chains.pem \
  -no_alt_chains \
  -state \
  -status \
  -tls1_1

# For macOS Homebrew OpenSSL
#
# $ openssl version
# OpenSSL 1.0.2k  26 Jan 2017
#
# $ openssl s_client --help
# unknown option --help
# usage: s_client args
# 
#  -host host     - use -connect instead
#  -port port     - use -connect instead
#  -connect host:port - who to connect to (default is localhost:4433)
#  -verify_hostname host - check peer certificate matches "host"
#  -verify_email email - check peer certificate matches "email"
#  -verify_ip ipaddr - check peer certificate matches "ipaddr"
#  -verify arg   - turn on peer certificate verification
#  -verify_return_error - return verification errors
#  -cert arg     - certificate file to use, PEM format assumed
#  -certform arg - certificate format (PEM or DER) PEM default
#  -key arg      - Private key file to use, in cert file if
#                  not specified but cert file is.
#  -keyform arg  - key format (PEM or DER) PEM default
#  -pass arg     - private key file pass phrase source
#  -CApath arg   - PEM format directory of CA's
#  -CAfile arg   - PEM format file of CA's
#  -no_alt_chains - only ever use the first certificate chain found
#  -reconnect    - Drop and re-make the connection with the same Session-ID
#  -pause        - sleep(1) after each read(2) and write(2) system call
#  -prexit       - print session information even on connection failure
#  -showcerts    - show all certificates in the chain
#  -debug        - extra output
#  -msg          - Show protocol messages
#  -nbio_test    - more ssl protocol testing
#  -state        - print the 'ssl' states
#  -nbio         - Run with non-blocking IO
#  -crlf         - convert LF from terminal into CRLF
#  -quiet        - no s_client output
#  -ign_eof      - ignore input eof (default when -quiet)
#  -no_ign_eof   - don't ignore input eof
#  -psk_identity arg - PSK identity
#  -psk arg      - PSK in hex (without 0x)
#  -srpuser user     - SRP authentification for 'user'
#  -srppass arg      - password for 'user'
#  -srp_lateuser     - SRP username into second ClientHello message
#  -srp_moregroups   - Tolerate other than the known g N values.
#  -srp_strength int - minimal length in bits for N (default 1024).
#  -ssl2         - just use SSLv2
#  -ssl3         - just use SSLv3
#  -tls1_2       - just use TLSv1.2
#  -tls1_1       - just use TLSv1.1
#  -tls1         - just use TLSv1
#  -dtls1        - just use DTLSv1
#  -fallback_scsv - send TLS_FALLBACK_SCSV
#  -mtu          - set the link layer MTU
#  -no_tls1_2/-no_tls1_1/-no_tls1/-no_ssl3/-no_ssl2 - turn off that protocol
#  -bugs         - Switch on all SSL implementation bug workarounds
#  -cipher       - preferred cipher to use, use the 'openssl ciphers'
#                  command to see what is available
#  -starttls prot - use the STARTTLS command before starting TLS
#                  for those protocols that support it, where
#                  'prot' defines which one to assume.  Currently,
#                  only "smtp", "pop3", "imap", "ftp" and "xmpp"
#                  are supported.
#  -engine id    - Initialise and use the specified engine
#  -rand file:file:...
#  -sess_out arg - file to write SSL session to
#  -sess_in arg  - file to read SSL session from
#  -servername host  - Set TLS extension servername in ClientHello
#  -tlsextdebug      - hex dump of all TLS extensions received
#  -status           - request certificate status from server
#  -no_ticket        - disable use of RFC4507bis session tickets
#  -serverinfo types - send empty ClientHello extensions (comma-separated numbers)
#  -curves arg       - Elliptic curves to advertise (colon-separated list)
#  -sigalgs arg      - Signature algorithms to support (colon-separated list)
#  -client_sigalgs arg - Signature algorithms to support for client
#                        certificate authentication (colon-separated list)
#  -nextprotoneg arg - enable NPN extension, considering named protocols supported (comma-separated list)
#  -alpn arg         - enable ALPN extension, considering named protocols supported (comma-separated list)
#  -legacy_renegotiation - enable use of legacy renegotiation (dangerous)
#  -use_srtp profiles - Offer SRTP key management with a colon-separated profile list
#  -keymatexport label   - Export keying material using label
#  -keymatexportlen len  - Export len bytes of keying material (default 20)
