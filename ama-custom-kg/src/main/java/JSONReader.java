import java.io.FileReader;

import org.apache.jena.rdf.model.Resource;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JSONReader {
    public static void parseEmployeeObject(JSONObject employee) {
        Resource danHarkey
                = Test.MODEL.createResource(Test.AMA_BASE + "/" + employee.get("sjsuId"));

        //System.out.println(employee.keySet());

        for (Object key: employee.keySet()) {
            System.out.println("key: " + key + " val: " + employee.get(key));
            danHarkey.addProperty(Test.personelMap.get(key), employee.get(key).toString());
        }

        Test.printRDFObject();
    }

    public static void readJSONFile() {
        JSONParser jsonParser = new JSONParser();

        try (FileReader reader = new FileReader(JSONReader.class.getResource("sjsu-entities.json").getFile()))
        {
            //Read JSON file
            JSONObject obj = (JSONObject) jsonParser.parse(reader);

            JSONArray employeeList = (JSONArray) obj.get("personel");
            //System.out.println(employeeList);

            //Iterate over employee array
            employeeList.forEach( emp -> parseEmployeeObject( (JSONObject) emp ) );
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String []args) {
        readJSONFile();
    }
}
