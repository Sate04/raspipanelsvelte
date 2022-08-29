const { app, BrowserWindow, ipcMain } = require("electron");
const { join } = require("path")

const isDev = !app.isPackaged;
app.whenReady().then(main);

function main () {
    const window = new BrowserWindow({
        width: 800,
        height: 600, show: false,
        autoHideMenuBar: true,
        webPreferences: {
            preload: join(__dirname, "./preload.js")
        }
    });

    window.loadFile(join(__dirname, "../public/index.html"));
    window.on("ready-to-show", window.show);

    if( isDev) window.webContents.openDevTools();
}