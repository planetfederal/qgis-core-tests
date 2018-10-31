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

# use `openssl s_server --help` to verify specific options
# options in order of --help output

# see -www, -WWW and -HTTP differences below
# if using -WWW, request GET/test.html
openssl s_server \
  -accept 4443 \
  -Verify 5 \
  -verify_return_error \
  -cert ${TEST_CERTS}/server-wildcard-boundless-test-cert.pem \
  -key ${TEST_CERTS}/server-wildcard-boundless-test-key.pem \
  -state \
  -CAfile ${TEST_CERTS}/subissuer-issuer-root-ca_issuer-2-root-2-ca_chains.pem \
  -no_alt_chains \
  -no_ssl2 \
  -no_ssl3 \
  -www

# For macOS Homebrew OpenSSL
#
# $ /usr/local/opt/openssl/bin/openssl version
# OpenSSL 1.0.2k  26 Jan 2017
#
# $ /usr/local/opt/openssl/bin/openssl s_server --help
# unknown option --help
# usage: s_server [args ...]
# 
#  -accept arg   - port to accept on (default is 4433)
#  -verify_hostname host - check peer certificate matches "host"
#  -verify_email email - check peer certificate matches "email"
#  -verify_ip ipaddr - check peer certificate matches "ipaddr"
#  -context arg  - set session ID context
#  -verify arg   - turn on peer certificate verification
#  -Verify arg   - turn on peer certificate verification, must have a cert.
#  -verify_return_error - return verification errors
#  -cert arg     - certificate file to use
#                  (default is server.pem)
#  -serverinfo arg - PEM serverinfo file for certificate
#  -auth               - send and receive RFC 5878 TLS auth extensions and supplemental data
#  -auth_require_reneg - Do not send TLS auth extensions until renegotiation
#  -no_resumption_on_reneg - set SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION flag
#  -crl_check    - check the peer certificate has not been revoked by its CA.
#                  The CRL(s) are appended to the certificate file
#  -crl_check_all - check the peer certificate has not been revoked by its CA
#                  or any other CRL in the CA chain. CRL(s) are appened to the
#                  the certificate file.
#  -certform arg - certificate format (PEM or DER) PEM default
#  -key arg      - Private Key file to use, in cert file if
#                  not specified (default is server.pem)
#  -keyform arg  - key format (PEM, DER or ENGINE) PEM default
#  -pass arg     - private key file pass phrase source
#  -dcert arg    - second certificate file to use (usually for DSA)
#  -dcertform x  - second certificate format (PEM or DER) PEM default
#  -dkey arg     - second private key file to use (usually for DSA)
#  -dkeyform arg - second key format (PEM, DER or ENGINE) PEM default
#  -dpass arg    - second private key file pass phrase source
#  -dhparam arg  - DH parameter file to use, in cert file if not specified
#                  or a default set of parameters is used
#  -named_curve arg  - Elliptic curve name to use for ephemeral ECDH keys.
#                  Use "openssl ecparam -list_curves" for all names
#                  (default is nistp256).
#  -nbio         - Run with non-blocking IO
#  -nbio_test    - test with the non-blocking test bio
#  -crlf         - convert LF from terminal into CRLF
#  -debug        - Print more output
#  -msg          - Show protocol messages
#  -state        - Print the SSL states
#  -CApath arg   - PEM format directory of CA's
#  -CAfile arg   - PEM format file of CA's
#  -no_alt_chains - only ever use the first certificate chain found
#  -nocert       - Don't use any certificates (Anon-DH)
#  -cipher arg   - play with 'openssl ciphers' to see what goes here
#  -serverpref   - Use server's cipher preferences
#  -quiet        - No server output
#  -no_tmp_rsa   - Do not generate a tmp RSA key
#  -psk_hint arg - PSK identity hint to use
#  -psk arg      - PSK in hex (without 0x)
#  -srpvfile file      - The verifier file for SRP
#  -srpuserseed string - A seed string for a default user salt.
#  -ssl2         - Just talk SSLv2
#  -ssl3         - Just talk SSLv3
#  -tls1_2       - Just talk TLSv1.2
#  -tls1_1       - Just talk TLSv1.1
#  -tls1         - Just talk TLSv1
#  -dtls1        - Just talk DTLSv1
#  -dtls1_2      - Just talk DTLSv1.2
#  -timeout      - Enable timeouts
#  -mtu          - Set link layer MTU
#  -chain        - Read a certificate chain
#  -no_ssl2      - Just disable SSLv2
#  -no_ssl3      - Just disable SSLv3
#  -no_tls1      - Just disable TLSv1
#  -no_tls1_1    - Just disable TLSv1.1
#  -no_tls1_2    - Just disable TLSv1.2
#  -no_dhe       - Disable ephemeral DH
#  -no_ecdhe     - Disable ephemeral ECDH
#  -bugs         - Turn on SSL bug compatibility
#  -hack         - workaround for early Netscape code
#  -www          - Respond to a 'GET /' with a status page
#  -WWW          - Respond to a 'GET /<path> HTTP/1.0' with file ./<path>
#  -HTTP         - Respond to a 'GET /<path> HTTP/1.0' with file ./<path>
#                  with the assumption it contains a complete HTTP response.
#  -engine id    - Initialise and use the specified engine
#  -id_prefix arg - Generate SSL/TLS session IDs prefixed by 'arg'
#  -rand file:file:...
#  -servername host - servername for HostName TLS extension
#  -servername_fatal - on mismatch send fatal alert (default warning alert)
#  -cert2 arg    - certificate file to use for servername
#                  (default is server2.pem)
#  -key2 arg     - Private Key file to use for servername, in cert file if
#                  not specified (default is server2.pem)
#  -tlsextdebug  - hex dump of all TLS extensions received
#  -no_ticket    - disable use of RFC4507bis session tickets
#  -legacy_renegotiation - enable use of legacy renegotiation (dangerous)
#  -sigalgs arg      - Signature algorithms to support (colon-separated list)
#  -client_sigalgs arg  - Signature algorithms to support for client 
#                         certificate authentication (colon-separated list)
#  -nextprotoneg arg - set the advertised protocols for the NPN extension (comma-separated list)
#  -use_srtp profiles - Offer SRTP key management with a colon-separated profile list
#  -alpn arg  - set the advertised protocols for the ALPN extension (comma-separated list)
#  -keymatexport label   - Export keying material using label
#  -keymatexportlen len  - Export len bytes of keying material (default 20)
#  -status           - respond to certificate status requests
#  -status_verbose   - enable status request verbose printout
#  -status_timeout n - status request responder timeout
#  -status_url URL   - status request fallback URL