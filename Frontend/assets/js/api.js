const API_BASE_URL = "http://127.0.0.1:8000/api";

const API = {
  login: `${API_BASE_URL}/auth/login/`,
  register: `${API_BASE_URL}/auth/register/`,
  me: `${API_BASE_URL}/auth/me/`,
  customerDashboard: `${API_BASE_URL}/customers/dashboard/`,
  providerDashboard: `${API_BASE_URL}/providers/dashboard/`,
  customerBookings: `${API_BASE_URL}/bookings/customer/`,
  providerBookings: `${API_BASE_URL}/bookings/provider/`,

  services: `${API_BASE_URL}/services/`,
  bookings: `${API_BASE_URL}/bookings/`,
  reviews: `${API_BASE_URL}/reviews/`,
  favorites: `${API_BASE_URL}/favorites/`,
  notifications: `${API_BASE_URL}/notifications/`,
  search: `${API_BASE_URL}/search/`,
  refresh: `${API_BASE_URL}/auth/refresh/`,
};
