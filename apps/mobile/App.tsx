import React from "react";
import { Text, TouchableOpacity, View } from "react-native";

export default function App() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#000",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text
        style={{
          color: "#FFF",
          fontSize: 32,
        }}
      >
        LICEU Academia
      </Text>
      <TouchableOpacity
        style={{
          backgroundColor: "#FFF",
          padding: 20,
          borderRadius: 20,
          marginTop: 20,
        }}
      >
        <Text>Iniciar Jornada</Text>
      </TouchableOpacity>
    </View>
  );
}
