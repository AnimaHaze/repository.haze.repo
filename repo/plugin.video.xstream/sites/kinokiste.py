
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('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')))).decode('utf-8'))
