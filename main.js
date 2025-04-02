const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      contextIsolation: true,
    }
  });

  win.loadURL('http://localhost:8501');
}

app.whenReady().then(() => {
  // Start the Streamlit server
  spawn('streamlit', ['run', 'Nutrition_Assistant.py'], {
    shell: true,
    env: process.env,
    stdio: 'inherit'
  });

  createWindow();
});
