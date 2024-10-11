import { createRouter, createWebHistory } from "vue-router";
import Korisnici from "@/views/Korisnici.vue";
import KorisnikNovi from "@/views/KorisnikNovi.vue";
import KorisnikIzmena from "@/views/KorisnikIzmena.vue";
import Login from "@/views/Login.vue";
import Predmeti from "@/views/Predmeti.vue";
import Studenti from "@/views/Studenti.vue";
import StudentNovi from "@/views/StudentNovi.vue";
import StudentIzmena from "@/views/StudentIzmena.vue";
import Student from "@/views/Student.vue";
import PredmetNovi from "@/views/PredmetNovi.vue";
import PredmetIzmena from "@/views/PredmetIzmena.vue";
import ProductsPrimer from "@/views/ProductsPrimer.vue";

const routes = [
  {
    path: "/korisnici",
    name: "Korisnici",
    component: Korisnici,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/korisnik-novi",
    name: "KorisnikNovi",
    component: KorisnikNovi,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/korisnik-izmena/:id",
    name: "KorisnikIzmena",
    component: KorisnikIzmena,
    props: true,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/predmeti",
    name: "Predmeti",
    component: Predmeti,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/predmet-novi",
    name: "PredmetNovi",
    component: PredmetNovi,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/predmet-izmena/:id",
    name: "PredmetIzmena",
    component: PredmetIzmena,
    props: true,
    meta: { requiresRole: ["administrator"] },
  },
  {
    path: "/studenti",
    name: "Studenti",
    component: Studenti,
    meta: { requiresRole: ["administrator", "profesor"] },
  },
  {
    path: "/student-novi",
    name: "StudentNovi",
    component: StudentNovi,
    meta: { requiresRole: ["administrator", "profesor"] },
  },
  {
    path: "/student-izmena/:id",
    name: "StudentIzmena",
    component: StudentIzmena,
    props: true,
    meta: { requiresRole: ["administrator", "profesor"] },
  },
  {
    path: "/student/:id",
    name: "Student",
    component: Student,
    props: true,
    meta: { requiresRole: ["administrator", "profesor"] },
  },
  {
    path: "/products",
    name: "Products",
    component: ProductsPrimer,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const role = localStorage.getItem("rola");

  if (role) {
    if (to.meta.requiresRole && !to.meta.requiresRole.includes(role)) {
      return next("/studenti");
    }
  } else if (to.meta.requiresRole) {
    return next("/login");
  }

  next();
});

export default router;
