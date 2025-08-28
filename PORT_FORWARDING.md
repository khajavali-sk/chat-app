# Port Forwarding Guide for Quantum Chat App

This guide explains how to make your Quantum Chat application accessible from different networks.

## Option 1: Router Port Forwarding (For Home Networks)

If you want to expose your app directly through your home router:

1. **Find your local IP address**:

   - Open Command Prompt and type `ipconfig`
   - Look for the "IPv4 Address" under your active network connection
   - Example: `192.168.1.100`

2. **Access your router's admin page**:

   - This is typically at http://192.168.1.1 or http://192.168.0.1
   - Enter your router admin credentials (check your router for details)

3. **Set up port forwarding**:

   - Look for "Port Forwarding" or "Virtual Server" settings
   - Create two new port forwarding rules:
     - Forward external port 5173 to internal port 5173 at your IP (for frontend)
     - Forward external port 8000 to internal port 8000 at your IP (for backend)
   - Save the settings

4. **Find your public IP address**:

   - Visit [whatismyip.com](https://www.whatismyip.com/)
   - Note down your public IP address

5. **Access your app**:
   - From the internet: `http://YOUR_PUBLIC_IP:5173`

**Note**: Most home ISPs provide dynamic IP addresses that change over time. Consider using a DDNS (Dynamic DNS) service like No-IP or DynDNS if you need a persistent address.

**Security Warning**: This method exposes your computer directly to the internet. Ensure you have proper security measures in place (firewall, updated software, etc.).

## Option 2: Use ngrok (Easiest Method)

Ngrok creates a secure tunnel to expose your local server to the internet:

1. **Download & Install ngrok**:

   - Visit [ngrok.com/download](https://ngrok.com/download)
   - Install the appropriate version for Windows
   - Sign up for a free account to get your authtoken

2. **Run the tunnel.bat script**:

   - Open Command Prompt in the project folder
   - Run `tunnel.bat`
   - Ngrok will provide a public URL (like `https://a1b2c3d4.ngrok.io`)

3. **Share the URL**:
   - Anyone on any network can now access your app using the ngrok URL
   - The WebSocket connection will automatically work through the tunnel

**Note**: Free ngrok account URLs expire after 2 hours and change each time you restart ngrok.

## Option 3: Cloud Deployment

For a permanent solution, consider deploying your application to a cloud provider:

- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Heroku, Render, DigitalOcean, AWS, Azure

This requires adapting the application for production deployment but provides the most reliable access from different networks.

## Troubleshooting

If you're having connection issues:

1. Make sure both frontend and backend servers are running
2. Check your firewall settings and allow the required ports
3. Verify your router's port forwarding configuration
4. Try accessing with both IP address and localhost
5. Check browser console for WebSocket connection errors
