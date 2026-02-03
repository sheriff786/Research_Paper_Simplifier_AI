const fs = require("fs");
const path = require("path");

const STRUCTURE = {
  "src/app": {
    "page.jsx": "",
    "layout.jsx": "",
    "dashboard/page.jsx": "",
    "chat/page.jsx": ""
  },
  "src/components": {
    "UploadBox.jsx": "",
    "SectionTabs.jsx": "",
    "SummaryCard.jsx": "",
    "CitationBox.jsx": "",
    "ChatWindow.jsx": "",
    "Loader.jsx": ""
  },
  "src/services": {
    "api.js": "",
    "endpoints.js": ""
  },
  "src/styles": {
    "globals.css": ""
  },
  "src/utils": {
    "constants.js": ""
  }
};

function create(base, tree) {
  for (const name in tree) {
    const target = path.join(base, name);
    if (typeof tree[name] === "string") {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      if (!fs.existsSync(target)) fs.writeFileSync(target, "");
    } else {
      fs.mkdirSync(target, { recursive: true });
      create(target, tree[name]);
    }
  }
}

create(process.cwd(), STRUCTURE);
console.log("✅ Frontend structure created");
