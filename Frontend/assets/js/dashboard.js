// =============================
// Check Login
// =============================
console.log(API);
const token = localStorage.getItem("access");

if (!token) {
  window.location.href = "login.html";
}

// =============================
// Load Current User
// =============================

async function loadUser() {
  try {
    const response = await fetch(API.me, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      localStorage.clear();

      window.location.href = "login.html";

      return;
    }

    const user = await response.json();

    document.getElementById("username").innerText =
      `${user.first_name} ${user.last_name}`;
  } catch (error) {
    console.log(error);
  }
}

// =============================
// Load Bookings
// =============================

async function loadBookings() {
  try {
    const response = await fetch(API.customerBookings, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Cannot load bookings");
    }

    const bookings = await response.json();

    document.getElementById("totalBookings").innerText = bookings.length;

    let pending = 0;
    let completed = 0;
    let cancelled = 0;

    bookings.forEach((booking) => {
      if (booking.status === "PENDING") pending++;

      if (booking.status === "COMPLETED") completed++;

      if (booking.status === "CANCELLED") cancelled++;
    });

    document.getElementById("pendingBookings").innerText = pending;

    document.getElementById("completedBookings").innerText = completed;

    document.getElementById("cancelledBookings").innerText = cancelled;

    const bookingList = document.getElementById("bookingList");

    bookingList.innerHTML = "";

    if (bookings.length === 0) {
      bookingList.innerHTML = `
                <div class="alert alert-info">
                    No bookings found.
                </div>
            `;

      return;
    }

    bookings.forEach((booking) => {
      bookingList.innerHTML += `

<div class="card shadow-sm mb-3">

    <div class="card-body">

        <div class="d-flex justify-content-between">

            <div>

                <h5 class="mb-1">

                    ${booking.service_name}

                </h5>

                <small class="text-muted">

                    Provider :
                    ${booking.provider_name}

                </small>

                <br>

                <small>

                    📅 ${booking.booking_date}

                </small>

                <br>

                <small>

                    🕒 ${booking.booking_time}

                </small>

                <br>

                <small>

                    📍 ${booking.address}

                </small>

            </div>

            <div class="text-end">

                <h5>

                    Rs. ${booking.total_price}

                </h5>

                <span class="badge bg-primary">

                    ${booking.status}

                </span>

            </div>

        </div>

    </div>

</div>

`;
    });
  } catch (error) {
    console.log(error);
  }
}

// =============================
// Logout
// =============================

document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.clear();

  window.location.href = "login.html";
});

// =============================

loadUser();

loadBookings();
