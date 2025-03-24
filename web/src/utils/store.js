const localStore = {
  set(key, value, ttl=60*60*1000) {
    const now = Date.now();
    const item = {
      value: value,
      expiry: now + ttl, // ms
    };
    localStorage.setItem(key, JSON.stringify(item));
  },

  get(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) return null;

    try {
      const item = JSON.parse(itemStr);
      if (Date.now() > item.expiry) {
        localStorage.removeItem(key); // auto remove after expiry
        return null;
      }
      return item.value;
    } catch (e) {
      console.error("Error parsing localStorage data:", e);
      return null;
    }
  },

  remove(key) {
    localStorage.removeItem(key);
  }
};

export default localStore;
