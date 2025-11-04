const url = "https://pythonlab.blackisland-5162e9b0.polandcentral.azurecontainerapps.io/doctors"; 

const TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsImV4cCI6MTc2MjM4MDA4NH0.KIrHvCDyarVPu17ZNNxaNT5VEbXcC4P7hLkchVcIUr8"; 

const data = {
  name: "LoadTest Equipment",
  description: "Created by load test",
  status: "Available",
  equipment_item_id: 1
};

async function sendRequest(i) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${TOKEN}`
    },
    body: JSON.stringify(data)
  });
  console.log(`Request ${i + 1}: ${res.status}`);
}

(async () => {
  const tasks = [];
  for (let i = 0; i < 1000; i++) {
    tasks.push(sendRequest(i));
  }
  await Promise.all(tasks);
})();