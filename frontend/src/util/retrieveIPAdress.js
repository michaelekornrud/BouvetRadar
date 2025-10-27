import { networkInterfaces } from 'os';

/**
 * Get the first non-internal IPv4 address.
 * Works on Mac, Windows, and Linux.
 */
export function collectIp() {
    const nets = networkInterfaces();
    
    for (const name of Object.keys(nets)) {
        for (const net of nets[name]) {
            // Skip internal (loopback) and IPv6
            if (net.family === 'IPv4' && !net.internal) {
                return net.address;
            }
        }
    }
    
    return null; // No suitable IP found
}

// If run directly (not imported)
if (import.meta.url === `file://${process.argv[1]}`) {
    console.log(collectIp() || 'No local IP found');
}