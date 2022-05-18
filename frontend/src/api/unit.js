import { HTTP } from "@/api/common";

export const Unit = {
  async list() {
    const response = await HTTP.get("units/");
    return response;
  },
};
