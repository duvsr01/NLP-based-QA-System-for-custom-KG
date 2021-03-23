import java.io.FileReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.apache.jena.rdf.model.*;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JSONReader {
    public static void parseDatabaseObject(JSONObject employee, Map<String, Property> entityMap) {
        Resource danHarkey
                = Test.MODEL.createResource(Test.AMA_BASE + "/" + employee.get("sjsuId"));

        //System.out.println(employee.keySet());
        for (Object key: employee.keySet()) {
            System.out.println("key: " + key + " val: " + employee.get(key));
            if (entityMap.containsKey(key)) {
                danHarkey.addProperty(entityMap.get(key), employee.get(key).toString());
            } else {
                String key_first_part = key.toString().split("_")[0];
                StmtIterator iter = Test.MODEL.listStatements( new SimpleSelector( null, Test.SJSU_ID_PROP, employee.get(key)) );

                if (iter.hasNext()) {
                    Statement resStemt = iter.nextStatement();
                    System.out.println("found: " + resStemt.getSubject());

                    if (entityMap.containsKey(key_first_part)) {
                        danHarkey.addProperty(entityMap.get(key_first_part), resStemt.getSubject());
                    }
                }
            }
        }

        Test.printRDFObject();
    }

    public static void readJSONFile() {
        JSONParser jsonParser = new JSONParser();

        ArrayList<String> entityCreationOrder = new ArrayList<>(
                Arrays.asList("department",
                        "course",
                        "personel"));

        try (FileReader reader = new FileReader(JSONReader.class.getResource("sjsu-entities.json").getFile())) {
            //Read JSON file
            JSONObject obj = (JSONObject) jsonParser.parse(reader);

            for (String entityType: entityCreationOrder) {
                JSONArray employeeList = (JSONArray) obj.get(entityType);

                Map<String, Property> entityMap = null;
                switch (entityType) {
                    case "department":
                        System.out.println("department");
                        entityMap = Test.departmentMap;
                        break;
                    case "personel":
                        entityMap = Test.personelMap;
                        break;
                    case "course":
                        entityMap = Test.courseMap;
                        break;
                    default:
                        System.out.println("default");
                        break;
                }

                if (entityMap != null) {
                    final Map<String, Property> finalEntityMap = entityMap;
                    employeeList.forEach(emp -> parseDatabaseObject((JSONObject) emp, finalEntityMap));
                }

            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String []args) {
        readJSONFile();
    }
}
