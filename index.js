const { app, BrowserWindow } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let mainWindow;
let streamlitProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(__dirname, "assets/icon.png"),
    webPreferences: {
      contextIsolation: true,
    },
  });

  mainWindow.loadURL("http://localhost:8501");

  mainWindow.on("closed", function () {
    mainWindow = null;
    if (streamlitProcess) {
      streamlitProcess.kill();
    }
  });
}

app.on("ready", () => {
  // Launch Streamlit
  streamlitProcess = spawn("streamlit", ["run", "Nutrition_Assistant.py"], {
    cwd: __dirname,
    shell: true,
  });

  streamlitProcess.stdout.on("data", (data) => {
    const msg = data.toString();
    console.log("Streamlit:", msg);

    if (msg.includes("Running on")) {
      // Open the window after the Streamlit server is ready
      createWindow();
    }
  });

  streamlitProcess.stderr.on("data", (data) => {
    console.error("Streamlit Error:", data.toString());
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", function () {
  if (mainWindow === null) {
    createWindow();
  }
});
