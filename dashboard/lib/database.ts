import * as mongoDB from "mongodb";
import { DataMode } from "./types";

const connectionString = `mongodb://${process.env.DATABASE_USER}:${process.env.DATABASE_PASSWORD}@db:27017/?retryWrites=true&w=majority`;

class Database {
  private static _realconnection: mongoDB.Db; // holds realtime data
  private static _highriskconnection: mongoDB.Db; // holds highrisk data

  private constructor() {}

  public static async getClient(mode: DataMode): Promise<mongoDB.Db> {
    if (!this._highriskconnection) {
      const client = new mongoDB.MongoClient(connectionString);

      await client.connect();

      this._highriskconnection = client.db("highrisk");
    }
    if (!this._realconnection) {
      const client = new mongoDB.MongoClient(connectionString);

      await client.connect();

      this._realconnection = client.db("realtime");
    }
    return mode === "realtime"
      ? this._realconnection
      : this._highriskconnection;
  }
}

export default Database;
