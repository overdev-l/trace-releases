import { readFileSync, writeFileSync } from 'node:fs'
import { randomBytes, createCipheriv, publicEncrypt, constants } from 'node:crypto'
const key = randomBytes(32), iv = randomBytes(12)
const cipher = createCipheriv('aes-256-gcm', key, iv)
const data = Buffer.concat([cipher.update(readFileSync(process.argv[2])), cipher.final()])
const wrapped = publicEncrypt({key: readFileSync(new URL('./diagnostics-public.pem', import.meta.url)), padding: constants.RSA_PKCS1_OAEP_PADDING, oaepHash: 'sha256'}, key)
writeFileSync(process.argv[2] + '.encrypted', JSON.stringify(Object.fromEntries(Object.entries({key: wrapped, iv, tag: cipher.getAuthTag(), data}).map(([k,v]) => [k,v.toString('base64')]))))
