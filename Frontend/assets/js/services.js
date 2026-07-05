const services = [
  {
    image: "images/service1.jpg",
    name: "Hair Cut",
    category: "Salon",
    price: 500,
    status: "Active",
  },

  {
    image: "images/service2.jpg",
    name: "Massage",
    category: "Therapy",
    price: 1200,
    status: "Inactive",
  },

  {
    image: "images/service3.jpg",
    name: "Facial",
    category: "Beauty",
    price: 900,
    status: "Active",
  },
];

const table = document.getElementById("serviceTable");

function displayServices(data) {
  table.innerHTML = "";

  data.forEach((service) => {
    table.innerHTML += `

        <tr>

        <td>
        <img src="${service.image}">
        </td>

        <td>${service.name}</td>

        <td>${service.category}</td>

        <td>Rs ${service.price}</td>

        <td>${service.status}</td>

        <td>

        <button class="edit">Edit</button>

        <button class="delete">Delete</button>

        </td>

        </tr>

        `;
  });
}

displayServices(services);

document.getElementById("searchService").addEventListener("keyup", (e) => {
  const keyword = e.target.value.toLowerCase();

  const filtered = services.filter((service) =>
    service.name.toLowerCase().includes(keyword),
  );

  displayServices(filtered);
});
